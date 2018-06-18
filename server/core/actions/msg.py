from protocol.server import Response
from protocol.codes import BASIC_NOTICE, SERVER_ERROR


def msg_processing(server_obj, message):
    """
    # Текстовое сообщение. может быть групповым или личным. содержит имя отправителя, имя получателя, тело сообщения
    # Ответ сервера:
    # 100 - сообщение отправлено
    # 101 - сообщение не доставлено
    :param server_obj:
    :param message:
    :return: Response
    """
    recipient = message.headers['recipient']
    response_message = Response(code=BASIC_NOTICE, action=message.action, body=message.body)
    response_message.add_header('recipient', recipient)
    response_message.add_header('sender', message.headers['sender'])
    if recipient.startswith('#'):
        # TODO async for
        for chat_member in server_obj.chat_controller.get_list_users(recipient):
            chat_member.send_message(response_message)
        return Response(code=BASIC_NOTICE, action=message.action, body=f'Message to {recipient} was sent successful')
    elif recipient.startswith('@'):
        for user in server_obj.chat_controller.get_list_users():
            if user.get_account_name == recipient[1:]:  # символ @ не нужен
                user.send_message(response_message)
                return Response(code=BASIC_NOTICE, action=message.action,
                                body=f'Private message to {recipient} was sent successful')
    else:
        return Response(code=SERVER_ERROR, action=message.action, body='Server Error was happened')
