from protocol.client import Request
from protocol.codes import WRONG_REQUEST, NOT_FOUND, ACCEPTED
from protocol.crypto.utils import get_hash


def authenticate_response_processing(response_message, ui_instance):
    if response_message.code == WRONG_REQUEST:
        password = ui_instance.request_password('Type your password: ')
        return Request(action='authenticate', body=[ui_instance.get_active_account_name, get_hash(password)])
    elif response_message.code == NOT_FOUND:
        new_password = ui_instance.request_password('Type new password: ')
        return Request(action='registration', body=[ui_instance.get_active_account_name, get_hash(new_password)])
    elif response_message.code == ACCEPTED:
        ui_instance.print_help()
        return Request(action='join', body='')
