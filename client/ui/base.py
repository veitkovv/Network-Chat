from abc import ABCMeta, abstractmethod
import datetime


class BaseUI(metaclass=ABCMeta):

    @abstractmethod
    def display_chat_message(self):
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

    def request_account_name(self, dialog_message):
        pass

    def request_password(self, dialog_message):
        pass