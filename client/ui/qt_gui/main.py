import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from client.ui.qt_gui.design import Ui_MainWindow
from protocol.client import Response


class MainWindow(QMainWindow):

    def __init__(self, ui_controller):
        super().__init__()
        # отрисовка главного окна
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Получаем экземпляр класса, из которого будут иходить сигналы
        self._ui_controller = ui_controller
        self.link_signals()

    def link_signals(self):
        """Метод соединяющий сигналы от дочернего потока с логикой и слоты в основном потоке"""
        self._ui_controller.signals.request_account_name_signal.connect(self.request_account_name)
        self._ui_controller.signals.render_message_from_server_signal.connect(self.render_message_from_server)
        self._ui_controller.signals.request_password_signal.connect(self.request_password)

    @pyqtSlot(str)
    def request_account_name(self, dialog_message):
        account_name = self.new_dialog(title='Account name request', message=dialog_message)
        if account_name:
            self._ui_controller.account_name = account_name

    @pyqtSlot(str)
    def request_password(self, dialog_message):
        password = self.new_dialog(title='Password request', message=dialog_message, echo_mode=QLineEdit.Password)
        if password:
            self._ui_controller.account_password = password

    @pyqtSlot(bytes)
    def render_message_from_server(self, message):
        response_obj = Response(message)
        server_message = f'{self._ui_controller.timestamp_to_normal_date(response_obj.headers["time"])} ' \
                         f'SERVER MESSAGE: ' \
                         f'ACTION: {response_obj.action} ' \
                         f'CODE: {response_obj.code} : {response_obj.body}'
        self.ui.chatMessages.insertHtml(f'<font color="red">{server_message}</font><br>')

    @staticmethod
    def new_dialog(title, message, icon_path=None, echo_mode=QLineEdit.Normal):
        """
        Запрос данных от пользователя в режиме диалога
        """
        input_dialog = QInputDialog(None)
        input_dialog.setInputMode(QInputDialog.TextInput)
        input_dialog.setTextEchoMode(echo_mode)
        input_dialog.setWindowTitle(title)
        input_dialog.setLabelText(message)
        input_dialog.setWindowIcon(QIcon(icon_path))
        input_dialog.setFixedSize(300, 200)
        ok = input_dialog.exec_()
        text = input_dialog.textValue()
        if ok:
            return text
        else:
            # TODO придумать как обрабатывать
            pass


def create_main_window(ui_instance):
    app = QApplication(sys.argv)
    w = MainWindow(ui_instance)
    w.show()
    sys.exit(app.exec_())
