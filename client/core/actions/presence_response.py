from protocol.client import Request
from protocol.codes import *
from protocol.crypto.utils import get_hash


def presence_response_processing(response_message, account_name):
    if response_message.code == NOT_FOUND:
        new_password = input('Введите новый пароль: ')
        return Request(action='registration', body=[account_name, get_hash(new_password)])
    elif response_message.code == WRONG_REQUEST:
        new_account_name = input('Введите корректное имя учетной записи: ')
        if new_account_name:
            return Request(action='presence', body=new_account_name)
    elif response_message.code == SERVER_ERROR:
        pass
    elif response_message.code == UNAUTHORIZED:
        password = input('Введите свой пароль: ')
        return Request(action='authenticate', body=[account_name, get_hash(password)])
