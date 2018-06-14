import asyncio
from protocol.byte_stream_handler import pick_messages_from_stream, append_message_len_to_message
from protocol.crypto.aes import CipherAes
from protocol.crypto.utils import public_key_from_bytes, rsa_cipher_byte_string, get_session_key
from protocol.client import Request, Response
from client.log.logging import client_logger as log
from client.core.response_handler import response_handler
from protocol.codes import UNAUTHORIZED
from protocol.crypto.utils import get_hash


class AsyncClientManager(asyncio.Protocol):
    def __init__(self, loop, ui_instance):
        super().__init__()
        self.loop = loop
        self._transport = None
        self._pub_key = ''
        self._aes = CipherAes('')
        self._user_interface = ui_instance  # UI консольный или GUI

    def connection_made(self, transport):
        self._transport = transport
        self._aes.set_secret(get_session_key(32))

    def data_received(self, data):
        if data:
            for message in pick_messages_from_stream(data):
                self.process_message_manager(message)

    def connection_lost(self, exc):
        log.info('The server closed the connection; Stop the event loop')
        self.loop.stop()

    def process_key_exchange(self, received_rsa_public_key):
        """
        Метод шифрует публичным ключем ключ для симметричного шифрования AES , для дальнейшего обмена сообщениями
        :param received_rsa_public_key: публичный ключ RSA
        :return:
        """
        # Сохраняем публичный ключ, которым будем шифровать ключ длля симметричного шифра
        self._pub_key = public_key_from_bytes(received_rsa_public_key)
        # Шифруем ключ сессии публичным ключем
        ciphered_session_key = rsa_cipher_byte_string(self._aes.get_secret(), self._pub_key)
        # Длинна сообщения в начало сообщения
        ciphered_session_key_with_len = append_message_len_to_message(ciphered_session_key)
        # Отправляем ключ, которым будут шифроваться все последующие ссообщения
        self._transport.write(ciphered_session_key_with_len)

    def perform_presence(self):
        """Метод отправляет presence"""
        account_name = self._user_interface.request_account_name('Введите имя пользователя: ')
        self._user_interface.set_account_name(account_name)
        presence = Request(action='presence', body=account_name)
        self.send_message(presence)

    def unauthorized_response(self):
        password = self._user_interface.request_password(
            f'{self._user_interface.get_active_account_name}, введите свой пароль: ')
        return Request(action='authenticate', body=[self._user_interface.get_active_account_name, get_hash(password)])

    def process_message_manager(self, message):
        """
        Метод обработки сообщений.
        Если еше нет ключа, то запускается обмен ключами с сервером и отправляется presence
        в условии Else - расшифровывается сообщение и передается на обработку
        """
        if not self._pub_key:
            self.process_key_exchange(message)
            if not self._user_interface.get_active_account_name:
                self.perform_presence()
        else:
            deciphered_message = self._aes.decrypt(message)
            server_response = Response(deciphered_message)
            try:
                # Отображение ответа сервера
                self._user_interface.render_message_from_server(deciphered_message)
                # Чтобы не делать это в каждом action_response, проверяем авторизацию.
                if server_response.code == UNAUTHORIZED:
                    new_request = self.unauthorized_response()
                else:
                    new_request = response_handler[server_response.action](server_response, self._user_interface)
                self.send_message(new_request)
            except IndexError:
                log.info(f'Action {server_response.action} do not allowed')

    def send_message(self, message):
        """Дописывает в начало длинну сообщения, и затем отправляет"""
        ciphered_message_with_len = append_message_len_to_message(message.to_cipher_bytes(self._aes))
        self._transport.write(ciphered_message_with_len)

    async def get_console_messages(self, loop):
        """Метод для отправки введенных данных с клавиатуры"""
        while True:
            msg = await loop.run_in_executor(None, input, self._user_interface.user_input_string)
            print(msg)
            # self.send_message(msg.encode())

    # async def get_iu_messages(self, loop):
    #     def executor():
    #         while not self.is_open:
    #             pass
    #         self.gui = Gui(None, self)
    #         self.output = self.tkoutput  # Set client output to tk window
    #         self.output("Connected to {0}:{1}\n".format(*self.sockname))
    #         self.gui.mainloop()
    #         self.transport.close()  # If window closed, close connection
    #         self.loop.stop()
    #
    #     await loop.run_in_executor(None, executor)  # Run GUI in executor for simultanity
