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
            raise ValueError('Некорректное значение порта. Должно быть меньше 65535')
        elif value < 1024:
            raise ValueError('Некорректное значение порта. Нельзя занимать порты меньше 1024')
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
        if re.match(ACCOUNT_NAME_PATTERN, value):
            instance.__dict__[self.name] = value
        elif len(value) > ACCOUNT_NAME_MAX_LEN:
            raise UserNameIncorrect(f'Имя учетной записи должно быть менее {ACCOUNT_NAME_MAX_LEN} символов')
        else:
            raise UserNameIncorrect('Имя учетной записи должно содержать латинские буквы и цифры')
