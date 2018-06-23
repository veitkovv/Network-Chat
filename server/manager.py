import asyncio
from protocol.byte_stream_handler import pick_messages_from_stream, append_message_len_to_message
from protocol.server import Request, Response
from protocol.crypto.utils import generate_rsa_pair, rsa_decipher_byte_string
from protocol.codes import *
from server.core.user import User
from server.core.actions_handler import actions_handler
from server.authentication_requiered import authentication_required
from server.core.exceptions import DefaultChatLeaveError


class AsyncServerManager(asyncio.Protocol):
    def __init__(self, chat_controller):
        self.chat_controller = chat_controller
        self.user = User('Anonymous')

    def connection_made(self, transport):
        """
        Новое соединение:
        1) Сохраняем абстракцию сокет-соединения
        2) Генерируем пару ключей
        3) Отправляем клиенту публичный ключ
        """
        self.user.transport = transport
        self.user.public, self.user.private = generate_rsa_pair()
        key = append_message_len_to_message(self.user.public.exportKey())
        self.user.transport.write(key)

    def connection_lost(self, exc):
        """При потере коннекта пользователь удаляется из всех чатов, остальным приходит оповещение об этом"""
        print(f'Lost connection with client {self.user.account_name}. Reason: {exc}')
        for chat_name in self.chat_controller.chats:
            user_disconnected_message = f'{self.user.account_name} has left chat {chat_name}'
            print(user_disconnected_message)
            response_user_disconnected = Response(action='leave', code=IMPORTANT_NOTICE, body=user_disconnected_message)
            # Удаляем из чатов юзера, который отключился
            try:
                self.chat_controller.delete_user_from_chat(self.user, chat_name)
            except DefaultChatLeaveError:
                pass  # Этот чат покинуть можно только во время потери соединения
            for user in self.chat_controller.get_list_users(chat_name):
                # оповещаем юзеров в чатах об этом событии
                user.send_message(response_user_disconnected)
        self.user.transport.close()

    def data_received(self, data):
        """
        При получении потока байт метод берет длинну сообщения из начала и расклеивает сообщения,
        которые могли быть склеенными.
        """
        for message in pick_messages_from_stream(data):
            self.process_message(message)

    @authentication_required
    def process_action(self, client_request):
        return actions_handler[client_request.action](self, client_request)

    def process_message(self, message):
        if not self.user.aes.secret:
            # Первое сообщение от клиента - зашифрованный публичным ключем RSA ключ сессии,
            # которым будут шифроваться все последующие сообщения
            decrypted_key = rsa_decipher_byte_string(message, self.user.private)
            self.user.aes.secret = decrypted_key
        else:
            decrypted_message = self.user.aes.decrypt(message)
            print('processing message: ', decrypted_message)
            client_request = Request(decrypted_message)
            try:
                response_message = self.process_action(client_request)
                self.user.send_message(response_message)

            except KeyError:
                self.user.send_message(
                    Response(code=SERVER_ERROR, action=client_request.action,
                             body=f'Action {client_request.action} do not allowed (not implemented yet)'))
