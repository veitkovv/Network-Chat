from protocol.server import Response
from protocol.codes import *
from server.settings import DEFAULT_CHAT
from server.core.exceptions import ChatNotFound, UserAlreadyInChat


def join_processing(server_obj, message):
    """
    Запрос на присоединение к чату. содержит имя чата (пустой join = дефолтный чат).
    Ответ сервера:
    200 - успешное присоединение к чату
    404 - чат не найден
    409 - пользователь уже в чате
    500 - ошибка сервера
    :param message:
    :param server_obj:
    """
    account_name = server_obj.user.get_account_name
    chat_name = message.body
    if not chat_name:
        chat_name = DEFAULT_CHAT
    try:
        server_obj.chat_controller.add_user_to_chat(account_name, chat_name)
        response = Response(code=OK, action=message.action,
                            body=f'User "{account_name}" successfully added to chat "{chat_name}"')
        response.add_header('name', chat_name)
        return response
    except (ChatNotFound, UserAlreadyInChat) as e:
        return Response(code=e.code, action=message.action, body=e.text)
