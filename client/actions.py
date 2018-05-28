from client.log.logging import client_logger as log
from time import time
from protocol.client import Request
from collections import deque
from client.settings import ENCODING, MESSAGE_SIZE_NUM

class Sender:
    """
    Класс для отправки сообщений JIM через сокет

    """

    def __init__(self, sock):
        super().__init__()
        self._sock = sock
        self._account_name = None
        self._queue = deque()

    def set_account_name(self, account_name):
        self._account_name = account_name

    def send_next_message(self):
        try:
            message = self._queue.popleft()
            log.debug(f'Отправляю сообщение {message}')
            # считаем длинну сообщения
            message_len = f'{len(message):0{MESSAGE_SIZE_NUM}d}'
            self._sock.send(message_len.encode(ENCODING) + message)
        except IndexError:
            pass

    def append_message_to_queue(self, message_bytes):
        """
        Добавляет сообщение в очередь
        """
        self._queue.append(message_bytes)

    def send_message(self, message):
        """Метод отправляет сообщение"""
        message_time = round(float(time()), 4)
        message.add_header('time', message_time)
        message.add_header('account_name', self._account_name)
        log.debug(f'Добавляю в очередь сообщение: {message}')
        self.append_message_to_queue(message.to_bytes())

    def presence(self):
        """
        Отправляет presence, читает ответ.
        200 -> запрос на авторизацию
        401 -> запрос на регистрацию
        """
        presence = Request(action='presence', body=self._account_name)
        self.send_message(presence)

    def registration(self, new_password):
        """
        Запрос сервера на регистрацию.
        """

        if new_password is not None:
            # запрос на регистрацию
            reg_request = Request(action='registration', body=self._account_name)
            reg_request.add_header('password', new_password)
            self.send_message(reg_request)

    def authentication(self, password):
        """
        Запрос на авторизацию.
        """
        auth_request = Request(action='authenticate', body=password)
        self.send_message(auth_request)

    # def get_delayed_messages(self):
    #     """Запрос на оффлайн-сообщения"""
    #     request = Request(action=GET_DELAYED, body=self._account_name)
    #     self.send_message(request)

    # def get_avatar_request(self):
    #     """
    #     Запрос аватарки по имени.
    #     Сервер передает по сети изображение, которое клиент потом помещает в label для этого.
    #     """
    #     request = Request(action=GET_AVATAR, body=self._account_name)
    #     self.send_message(request)
    #
    # def get_active_chats(self):
    #     """
    #     запрос к серверу на список чатов, в которых участвует клиент
    #     """
    #     request = Request(action=GET_CHATS, body='')
    #     self.send_message(request)
    #
    # def get_chat_users(self, chat_name):
    #     """
    #     запрос серверу на список пользователей в чате по имени чата
    #     """
    #     request = Request(action=GET_CHAT_USERS, body=chat_name)
    #     self.send_message(request)
    #
    # def leave_chat(self, chat_name):
    #     """Запрос на выход из чата"""
    #     request = Request(action=LEAVE, body=chat_name)
    #     self.send_message(request)

    def get_contacts(self):
        """
        запрос на список контактов
        """
        request = Request(action='get_contacts', body='')
        self.send_message(request)

    def add_contact(self, contact):
        """Добавление контакта"""
        request = Request(action='add_contact', body=contact)
        self.send_message(request)

    def del_contact(self, contact):
        """Удаление контакта"""
        request = Request(action='del_contact', body=contact)
        self.send_message(request)

    def join_chat(self, chat_name, role='user'):
        """запрос на присоединение к чату"""
        request = Request(action='join', body=chat_name)
        request.add_header('role', role)
        self.send_message(request)

    def msg(self, message, to_):
        """Сообщение"""
        msg = Request(action='msg', body=message)
        msg.add_header('to', to_)
        self.send_message(msg)

    # def create_chat(self, new_chat_name):
    #     if not new_chat_name.startswith('#'):
    #         new_chat_name = f'#{new_chat_name}'
    #     request = Request(action=CREATE_CHAT, body=new_chat_name)
    #     self.send_message(request)
    #
    # def avatar_sample(self, sample, counter, quantity):
    #     request = Request(action=AVATAR_UPDATE, body=sample)
    #     request.add_header(MESSAGE_COUNTER, [counter, quantity])
    #     self.send_message(request)
