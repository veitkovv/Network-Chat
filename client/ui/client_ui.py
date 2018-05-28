# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(921, 630)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.contactTreeView = QtWidgets.QTreeView(self.centralwidget)
        self.contactTreeView.setMaximumSize(QtCore.QSize(200, 16777215))
        self.contactTreeView.setObjectName("contactTreeView")
        self.gridLayout.addWidget(self.contactTreeView, 1, 1, 2, 1)
        self.sendMessage = QtWidgets.QPushButton(self.centralwidget)
        self.sendMessage.setMinimumSize(QtCore.QSize(100, 0))
        self.sendMessage.setMaximumSize(QtCore.QSize(200, 30))
        self.sendMessage.setStyleSheet("QPushButton#Type1 {\n"
"     background-color: red;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 14px;\n"
"     min-width: 10em;\n"
"     padding: 6px;\n"
" }")
        self.sendMessage.setAutoExclusive(False)
        self.sendMessage.setAutoDefault(False)
        self.sendMessage.setDefault(False)
        self.sendMessage.setFlat(False)
        self.sendMessage.setObjectName("sendMessage")
        self.gridLayout.addWidget(self.sendMessage, 3, 1, 1, 1)
        self.chatMessages = QtWidgets.QTextEdit(self.centralwidget)
        self.chatMessages.setReadOnly(True)
        self.chatMessages.setObjectName("chatMessages")
        self.gridLayout.addWidget(self.chatMessages, 1, 0, 1, 1)
        self.inputMessage = QtWidgets.QTextEdit(self.centralwidget)
        self.inputMessage.setMaximumSize(QtCore.QSize(16777215, 30))
        self.inputMessage.setObjectName("inputMessage")
        self.gridLayout.addWidget(self.inputMessage, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 921, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.contactMenu = QtWidgets.QMenu(self.menu)
        self.contactMenu.setObjectName("contactMenu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.optionsMenu = QtWidgets.QAction(MainWindow)
        self.optionsMenu.setObjectName("optionsMenu")
        self.exitMenu = QtWidgets.QAction(MainWindow)
        self.exitMenu.setCheckable(False)
        self.exitMenu.setObjectName("exitMenu")
        self.addContactMenu = QtWidgets.QAction(MainWindow)
        self.addContactMenu.setObjectName("addContactMenu")
        self.delContact = QtWidgets.QAction(MainWindow)
        self.delContact.setObjectName("delContact")
        self.searchContact = QtWidgets.QAction(MainWindow)
        self.searchContact.setObjectName("searchContact")
        self.messageHistoryMenu = QtWidgets.QAction(MainWindow)
        self.messageHistoryMenu.setObjectName("messageHistoryMenu")
        self.loadAvatarMenu = QtWidgets.QAction(MainWindow)
        self.loadAvatarMenu.setObjectName("loadAvatarMenu")
        self.sendFileMenu = QtWidgets.QAction(MainWindow)
        self.sendFileMenu.setObjectName("sendFileMenu")
        self.contactMenu.addAction(self.addContactMenu)
        self.contactMenu.addAction(self.delContact)
        self.contactMenu.addAction(self.searchContact)
        self.menu.addAction(self.optionsMenu)
        self.menu.addAction(self.contactMenu.menuAction())
        self.menu.addAction(self.loadAvatarMenu)
        self.menu.addAction(self.exitMenu)
        self.menu_2.addAction(self.sendFileMenu)
        self.menu_2.addAction(self.messageHistoryMenu)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.contactTreeView.setToolTip(_translate("MainWindow", "<html><head/><body><p>Список контактов</p></body></html>"))
        self.sendMessage.setToolTip(_translate("MainWindow", "<html><head/><body><p>Отправить сообщение</p><p><br/></p></body></html>"))
        self.sendMessage.setText(_translate("MainWindow", "Отправить"))
        self.chatMessages.setToolTip(_translate("MainWindow", "<html><head/><body><p>Окно чата</p></body></html>"))
        self.inputMessage.setToolTip(_translate("MainWindow", "<html><head/><body><p>Поле ввода сообщения</p></body></html>"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.contactMenu.setTitle(_translate("MainWindow", "Контакты"))
        self.menu_2.setTitle(_translate("MainWindow", "Сообщения"))
        self.optionsMenu.setText(_translate("MainWindow", "Опции"))
        self.exitMenu.setText(_translate("MainWindow", "Выход"))
        self.addContactMenu.setText(_translate("MainWindow", "Добавить контакт"))
        self.delContact.setText(_translate("MainWindow", "Удалить контакт"))
        self.searchContact.setText(_translate("MainWindow", "Поиск контакта"))
        self.messageHistoryMenu.setText(_translate("MainWindow", "История сообщений"))
        self.loadAvatarMenu.setText(_translate("MainWindow", "Загрузить аватар"))
        self.sendFileMenu.setText(_translate("MainWindow", "Передать файл"))

