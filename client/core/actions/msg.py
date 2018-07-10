from protocol.codes import BASIC_NOTICE


def msg_response(response_message, ui_instance):
    if response_message.code == BASIC_NOTICE:  # обычное сообщение
        if response_message.headers['recipient'].startswith('#'):
            ui_instance.display_chat_message(response_message)
        elif response_message.headers['recipient'].startswith('@'):
            ui_instance.display_private_message(response_message)
    else:  # код какой-то ошибки
        ui_instance.display_error(response_message)
