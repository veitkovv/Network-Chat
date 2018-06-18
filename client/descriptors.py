# from protocol.actions import ACTIONS
#
#
# class ActionName:
#     """
#     Дескриптор для проверки action
#     """
#
#     def __init__(self):
#         self.action = None
#
#     def __get__(self, instance, owner):
#         return instance.__dict__[self.action]
#
#     def __set__(self, instance, value):
#         if value not in ACTIONS:
#             raise ValueError('Action отсутствует в протоколе')
#         else:
#             instance.__dict__[self.action] = value
