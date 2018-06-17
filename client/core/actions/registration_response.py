from protocol.client import Request
from protocol.codes import CONFLICT, WRONG_REQUEST, CREATED
from protocol.crypto.utils import get_hash


def registration_response_processing(response_message, ui_instance):
    ui_account_name = ui_instance.get_active_account_name
    if response_message.code == WRONG_REQUEST:
        new_password = ui_instance.request_password('Введите корректный пароль: ')
        return Request(action='registration', body=[ui_account_name, get_hash(new_password)])
    elif response_message.code == CONFLICT:
        new_account_name = ui_instance.request_account_name('Введите другое имя пользователя: ')
        ui_instance.set_account_name(new_account_name)
        new_password = ui_instance.request_password('Введите пароль: ')
        return Request(action='registration', body=[ui_account_name, get_hash(new_password)])
    elif response_message.code == CREATED:
        just_created_password = ui_instance.request_password('Введите пароль еще раз, чтобы авторизоваться: ')
        return Request(action='authenticate', body=[ui_account_name, get_hash(just_created_password)])
    else:
        print('unknown response', response_message)
