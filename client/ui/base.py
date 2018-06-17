from abc import ABCMeta, abstractmethod
import datetime


class BaseUI(metaclass=ABCMeta):

    def __init__(self):
        self._active_chat = None
        self._account_name = ''

    @abstractmethod
    def display_chat_message(self, message):
        pass

    @abstractmethod
    def display_private_message(self):
        pass

    @abstractmethod
    def display_contact_list(self):
        pass

    @abstractmethod
    def display_chat_list(self):
        pass

    @abstractmethod
    def display_chat_state(self):
        """join/leave chat message"""
        pass

    @abstractmethod
    def display_presence(self):
        pass

    @staticmethod
    def timestamp_to_normal_date(timestamp):
        return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

    @abstractmethod
    def request_account_name(self, dialog_message):
        pass

    @abstractmethod
    def request_password(self, dialog_message):
        pass

    @property
    def get_active_chat_name(self):
        return self._active_chat

    def set_active_chat_name(self, chat):
        if not chat.startswith('#'):
            self._active_chat = '#' + chat
        else:
            self._active_chat = chat

    @property
    def get_active_account_name(self):
        return self._account_name

    def set_account_name(self, account_name):
        self._account_name = account_name
