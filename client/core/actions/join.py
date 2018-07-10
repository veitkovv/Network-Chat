from protocol.client import Request
from protocol.codes import CONFLICT, NOT_FOUND, OK


def join_response(response_message, ui_controller):
    if response_message.code == NOT_FOUND:
        # Чат не найден. Запрос списка чатов.
        return Request(action='get_chats', body=ui_controller.account_name)
    elif response_message.code == CONFLICT:
        # пользователь уже в чате.
        pass
    elif response_message.code == OK:
        chat_name = response_message.headers['name']
        # print([method_name for method_name in dir(ui_instance) if callable(getattr(ui_instance, method_name))])
        ui_controller.current_chat = chat_name
