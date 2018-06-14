from server.descriptors import AccountName


class User:
    """Класс пользователя на сервере"""
    _account_name = AccountName()  # проверка валидности user-name

    def __init__(self, account_name):
        self._account_name = account_name
        self._transport = None
        self.public = None  # ключ rsa публичный
        self.private = None  # ключ rsa приватный
        self._authenticated = False  # если клиент прошел аутентификацию

    def __repr__(self):
        return f'User Object: {self._account_name} : {self._transport}'

    def set_account_name(self, account_name):
        self._account_name = account_name

    @property
    def get_account_name(self):
        return self._account_name

    def set_transport(self, transport):
        self._transport = transport

    @property
    def get_transport(self):
        return self._transport

    def set_authenticated(self):
        self._authenticated = True

    def set_unauthenticated(self):
        self._authenticated = False

    @property
    def is_authenticated(self):
        return self._authenticated
