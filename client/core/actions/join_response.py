from protocol.client import Request
from protocol.codes import CONFLICT, NOT_FOUND, OK


def join_response_processing(response_message, ui_instance):
    if response_message.code == NOT_FOUND:
        # Чат не найден. Запрос списка чатов.
        return Request(action='get_chats', body=ui_instance.account_name)
    elif response_message.code == CONFLICT:
        # пользователь уже в чате.
        pass
    elif response_message.code == OK:
        chat_name = response_message.headers['name']
        # print([method_name for method_name in dir(ui_instance) if callable(getattr(ui_instance, method_name))])
        ui_instance.current_chat = chat_name
