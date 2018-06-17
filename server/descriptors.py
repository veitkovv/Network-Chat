import re
from server.settings import PORT, ACCOUNT_NAME_PATTERN, ACCOUNT_NAME_MAX_LEN
from server.core.exceptions import UserNameIncorrect


class Port:
    """
    Дескриптор для проверки порта 1024 - 65535
    """

    def __init__(self):
        self.tcp_port = PORT

    def __get__(self, instance, owner):
        return instance.__dict__[self.tcp_port]

    def __set__(self, instance, value):
        if value > 65535:
            raise ValueError('Incorrect Port Value. It must be < 65535')
        elif value < 1024:
            raise ValueError('Incorrect Port Value. Port nums greater then 1024 do not allowed')
        else:
            instance.__dict__[self.tcp_port] = value


class AccountName:
    """
    Валидация account_name
    """

    def __init__(self):
        self.name = None

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if 0 > len(value) > ACCOUNT_NAME_MAX_LEN:
            raise UserNameIncorrect(
                f'Account name length must be between 0 and {ACCOUNT_NAME_MAX_LEN}. Your length: {len(value)}')
        elif not re.match(ACCOUNT_NAME_PATTERN, value):
            raise UserNameIncorrect('Account name must contain only latin letters and numbers')
        else:
            instance.__dict__[self.name] = value
