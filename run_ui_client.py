import sys
from client.ui.client_gui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class ClientQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ClientQt()
    w.show()
    sys.exit(app.exec_())
