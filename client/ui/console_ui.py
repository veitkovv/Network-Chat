from client.ui.base import BaseUI
from client.log.logging import client_logger as log
from protocol.client import Response
from time import time


class ConsoleClient(BaseUI):

    def __init__(self):
        self._active_chat = None
        self._account_name = None

    def display_chat_message(self):
        pass

    def display_private_message(self):
        pass

    def display_contact_list(self):
        pass

    def display_presence(self):
        pass

    def display_chat_list(self):
        pass

    def display_chat_state(self):
        pass

    @property
    def get_active_chat_name(self):
        return self._active_chat

    @property
    def get_active_account_name(self):
        return self._account_name

    def set_account_name(self, account_name):
        self._account_name = account_name

    @property
    def user_input_string(self):
        return f'{self.timestamp_to_normal_date(time())}: {self.get_active_account_name}: {self.get_active_chat_name}>>'

    @staticmethod
    def print_help():
        print('=' * 100)
        print('=' * 20, ' INFO ', '=' * 20)
        print('=' * 100)
        print('@username сообщение - личное сообщение')
        print('#chatname сообщение - сообщение в чат')
        print('+name - добавить контакт')
        print('-name - удалить контакт')
        print('/list - список контактов')
        print('/chatlist - список чатов')
        print('? - показать это сообщение')
        print('/exit /quit /logout - выход')
        print('=' * 100)
        print('=' * 20, ' END INFO ', '=' * 20)
        print('=' * 100)

    def render_message_from_server(self, message):
        log.debug(f'processing {message}')
        response_obj = Response(message)
        print(f'Time: {self.timestamp_to_normal_date(response_obj.headers["time"])} \n'
              f'Code: {response_obj.code} \n'
              f'Action: {response_obj.action} \n'
              f'Server Message: {response_obj.body}')
