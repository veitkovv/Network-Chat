from client.ui.base import BaseUI
from PyQt5.QtCore import pyqtSignal, QObject


class QtSignals(QObject):
    request_account_name_signal = pyqtSignal(str)
    render_message_from_server_signal = pyqtSignal(bytes)
    request_password_signal = pyqtSignal(str)


class GuiClient(BaseUI):

    def __init__(self):
        super().__init__()
        self.signals = QtSignals()

    def display_chat_message(self, message):
        pass

    def display_private_message(self, message):
        pass

    def display_error(self, message):
        pass

    def render_message_from_server(self, message):
        """Входящие сообщения от сервера будут отображаться в интерфейсе"""
        self.signals.render_message_from_server_signal.emit(message)

    def display_contact_list(self, message):
        pass

    def display_chat_list(self):
        pass

    def display_chat_state(self):
        pass

    def display_presence(self):
        pass

    def request_account_name(self, dialog_message):
        """Из дочернего потока с циклом событий отправляем сигнал главному окну
        В главном окне через диалог получаем имя пользователя и возвращаем его контроллеру"""
        self.signals.request_account_name_signal.emit(dialog_message)
        while not self.account_name:
            pass  # ждем ввода имени пользователя
        return self.account_name

    def request_password(self, dialog_message):
        """Если код ответа - 401 , то в диалоге будет запрошен пароль"""
        self.signals.request_password_signal.emit(dialog_message)
        while not self.account_password:
            pass  # ввод пользователя
        return self.account_password
