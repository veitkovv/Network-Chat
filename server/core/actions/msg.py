from protocol.server import Response
from protocol.codes import BASIC_NOTICE


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
    if recipient.startswith('#'):
        response_message = Response(code=BASIC_NOTICE, action=message.action, body=message.body)
        response_message.add_header('recipient', recipient)
        response_message.add_header('sender', message.headers['sender'])
        for chat_member in server_obj.chat_controller.get_list_users(recipient):
            chat_member.send_message(response_message)
        return Response(code=BASIC_NOTICE, action=message.action, body='Message was sent successful')
    else:
        response_message = Response(code=BASIC_NOTICE, action=message.action, body=message.body)
        response_message.add_header('recipient', recipient)
        response_message.add_header('sender', message.headers['sender'])
