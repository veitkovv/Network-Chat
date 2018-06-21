from protocol.client import Request
from protocol.codes import CONFLICT, NOT_FOUND, OK


def get_contacts_response_processing(response_message, ui_instance):
    print('=' * 20, response_message.body)
