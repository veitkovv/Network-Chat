from abc import ABCMeta, abstractmethod
import datetime


class BaseUI(metaclass=ABCMeta):

    def __init__(self):
        self._active_chat = None
        self._account_name = ''
        self._contact_list = list()

    @abstractmethod
    def display_chat_message(self, message):
        pass

    @abstractmethod
    def display_private_message(self, message):
        pass

    @abstractmethod
    def display_error(self, message):
        pass

    @abstractmethod
    def display_contact_list(self, message):
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
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, value):
        self._account_name = value

    @property
    def current_chat(self):
        return self._active_chat

    @current_chat.setter
    def current_chat(self, value):
        """Названия чатов должны начинаться с # """
        if not value.startswith('#'):
            self._active_chat = '#' + value
        else:
            self._active_chat = value

    @property
    def contact_list(self):
        return self._contact_list

    def add_contact_to_list(self, contact_name_to_add):
        self._contact_list.append(contact_name_to_add)

    def del_contact_from_list(self, contact_name_to_remove):
        self._contact_list.remove(contact_name_to_remove)
