from protocol.actions import ACTIONS


class ActionName:
    """
    Дескриптор для проверки action
    """

    def __init__(self):
        self.action = None

    def __get__(self, instance, owner):
        return instance.__dict__[self.action]

    def __set__(self, instance, value):
        if value not in ACTIONS:
            raise ValueError('Action отсутствует в протоколе')
        else:
            instance.__dict__[self.action] = value


# class AccountName:
#     """
#     Валидация account_name
#     """
#
#     def __init__(self):
#         self.name = None
#
#     def __get__(self, instance, owner):
#         return instance.__dict__[self.name]
#
#     def __set__(self, instance, value):
#         if re.match(ACCOUNT_NAME_PATTERN, value):
#             instance.__dict__[self.name] = value
#         else:
#             raise ValueError('Имя учетной записи должно содержать латинские буквы и цифры')
