from protocol.client import Request
from protocol.codes import WRONG_REQUEST, NOT_FOUND, ACCEPTED
from protocol.crypto.utils import get_hash


def authenticate_response_processing(response_message, ui_controller):
    if response_message.code == WRONG_REQUEST:
        password = ui_controller.request_password('Type your password: ')
        return Request(action='authenticate', body=[ui_controller.account_name, get_hash(password)])
    elif response_message.code == NOT_FOUND:
        new_password = ui_controller.request_password('Type new password: ')
        return Request(action='registration', body=[ui_controller.account_name, get_hash(new_password)])
    elif response_message.code == ACCEPTED:
        # ui_controller.print_help() TODO
        return Request(action='join', body='')
