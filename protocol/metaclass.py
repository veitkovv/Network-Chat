from protocol.actions import ACTIONS


# class ActionsMeta(type):
#     """
#     Чтобы следовать протоколу, метакласс проверяет есть ли в классе методы, реализующие actions
#     """
#
#     def __new__(cls, clsname, superclasses, attributedict):
#         callable_list = [i for i in attributedict if callable(attributedict[i])]
#         for action in ACTIONS:
#             if action not in callable_list:
#                 raise Exception(f'Method {action} did not implemented in class {clsname}')
#         return type.__new__(cls, clsname, superclasses, attributedict)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
