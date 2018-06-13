from server.descriptors import AccountName



class User:
    """Класс пользователя на сервере"""
    account_name = AccountName()  # проверка валидности user-name

    def __init__(self, account_name):
        self.account_name = account_name
        self.transport = None
        self.public = None  # ключ rsa публичный
        self.private = None  # ключ rsa приватный
        self.authenticated = False  # если клиент прошел аутентификацию

    def __repr__(self):
        return f'User Object: {self.account_name} : {self.transport}'

    def set_account_name(self, account_name):
        self.account_name = account_name

    def set_transport(self, transport):
        self.transport = transport


