import re
from server.settings import PORT, ACCOUNT_NAME_PATTERN


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
        else:
            raise ValueError('Имя учетной записи должно содержать латинские буквы и цифры')