from protocol.client import Request
from protocol.codes import NOT_FOUND, WRONG_REQUEST, SERVER_ERROR
from protocol.crypto.utils import get_hash


def presence_response_processing(response_message, ui_instance):
    if response_message.code == NOT_FOUND:
        new_password = ui_instance.request_password('Введите новый пароль: ')
        return Request(action='registration', body=[ui_instance.get_active_account_name, get_hash(new_password)])
    elif response_message.code == WRONG_REQUEST:
        new_account_name = ui_instance.request_account_name('Введите корректное имя учетной записи: ')
        ui_instance.set_account_name(new_account_name)
        return Request(action='presence', body=new_account_name)
    elif response_message.code == SERVER_ERROR:
        pass  # just show the message, nothing to do
    # elif response_message.code == UNAUTHORIZED:
    #     password = ui_instance.request_password(f'{ui_instance.get_active_account_name}, введите свой пароль: ')
    #     return Request(action='authenticate', body=[ui_instance.get_active_account_name, get_hash(password)])
