from client.ui.base import BaseUI
from client.log.logging import client_logger as log
from protocol.client import Request, Response
from time import time


class ConsoleClient(BaseUI):
    def __init__(self):
        super().__init__()

    def display_chat_message(self, message):
        out_string = f'\nCHAT MESSAGE {message.headers["recipient"]}: ' \
                     f'<{self.timestamp_to_normal_date(message.headers["time"])}> ' \
                     f'<FROM USER: {message.headers["sender"]}> ' \
                     f'{message.body}'
        print(out_string)

    def display_private_message(self, message):
        out_string = f'\nPRIVATE MESSAGE ' \
                     f'<{self.timestamp_to_normal_date(message.headers["time"])}> ' \
                     f'<FROM USER: {message.headers["sender"]}> ' \
                     f'{message.body}'
        print(out_string)

    def display_error(self, message):
        print(f'<{self.timestamp_to_normal_date(message.headers["time"])}> '
              f'Error! {message.body}')

    def display_contact_list(self):
        pass

    def display_presence(self):
        pass

    def display_chat_list(self):
        pass

    def display_chat_state(self):
        pass

    def request_account_name(self, dialog_message):
        return input(dialog_message)

    def request_password(self, dialog_message):
        return input(dialog_message)

    @property
    def user_input_string(self):
        return f'{self.timestamp_to_normal_date(time())}: {self.get_active_account_name}: {self.get_active_chat_name}>>'

    @staticmethod
    def print_help():
        print('=' * 48)
        print('=' * 20, ' INFO ', '=' * 20)
        print('=' * 48)
        print('@username some_msg - send a private message')
        print('#chatname some_msg - send a chat message (by default - message to current chat)')
        print('+name - add contact')
        print('-name - delete contact')
        print('/list - contact list')
        print('/chatlist - list of chats on the server')
        print('/join chat_name - join the chat_name')
        print('/leave chat_name - leave chat_name')
        print('? - display this message')
        print('/exit /quit /logout - exit')
        print('=' * 52)
        print('=' * 20, ' END INFO ', '=' * 20)
        print('=' * 52)

    def render_message_from_server(self, message):
        log.debug(f'processing {message}')
        response_obj = Response(message)
        if not response_obj.action == 'msg':
            print(f'SERVER MESSAGE:<< <{self.timestamp_to_normal_date(response_obj.headers["time"])}> '
                  f'<ACTION: {response_obj.action}> '
                  f'<CODE: {response_obj.code}> : {response_obj.body}')

    def keyboard_input_actions_manager(self, user_input_message):
        """
        Парсит ввод клавиатуры (согласно help), определяя тип сообщения, которое нужно отправить на сервер.
        :param user_input_message: введенный пользователем текст
        :return: Объект Request
        """
        if user_input_message.startswith('@'):
            recipient = user_input_message.split(' ')[0]
            action_msg = Request(action='msg', body=user_input_message[len(recipient):])
            action_msg.add_header('recipient', recipient)
            action_msg.add_header('sender', self.get_active_account_name)
            return action_msg
        elif user_input_message.startswith('#'):
            recipient = user_input_message.split(' ')[0]
            action_msg = Request(action='msg', body=user_input_message[len(recipient):])
            action_msg.add_header('recipient', recipient)
            action_msg.add_header('sender', self.get_active_account_name)
            return action_msg
        elif user_input_message.startswith('+'):
            new_contact = user_input_message.split(' ')[0][1:]
            return Request(action='add_contact', body=new_contact)
        elif user_input_message.startswith('-'):
            new_contact = user_input_message.split(' ')[0][1:]
            return Request(action='del_contact', body=new_contact)
        elif user_input_message.startswith('/list'):
            return Request(action='get_contacts', body='')
        elif user_input_message.startswith('/chatlist'):
            return Request(action='get_chats', body='')
        elif user_input_message.startswith('/join'):
            chat_name = user_input_message.split(' ')[1]
            return Request(action='join', body=chat_name)
        elif user_input_message.startswith('/leave'):
            chat_name = user_input_message.split(' ')[1]
            return Request(action='leave', body=chat_name)
        elif user_input_message.startswith('?'):
            self.print_help()
        elif user_input_message == '/exit' or user_input_message == '/quit' or user_input_message == '/logout':
            raise KeyboardInterrupt
        else:
            if self.get_active_chat_name is not None:
                # по умолчанию - сообщение в текущий чат
                action_msg = Request(action='msg', body=user_input_message)
                action_msg.add_header('recipient', self.get_active_chat_name)
                action_msg.add_header('sender', self.get_active_account_name)
                return action_msg
