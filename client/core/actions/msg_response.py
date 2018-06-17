def msg_response_processing(response_message, ui_instance):
    if response_message.headers['recipient'].startswith('#'):
        ui_instance.display_chat_message(response_message)
