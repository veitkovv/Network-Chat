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
    chat_name = message.body
    if not chat_name:  # Если приходит пустой join - понимаем как default chat
        chat_name = DEFAULT_CHAT
    try:
        server_obj.chat_controller.add_user_to_chat(server_obj.user, chat_name)  # Добавляем пользователя в чат
        response = Response(code=OK, action=message.action,
                            body=f'User "{server_obj.user.get_account_name}" successfully joined chat {chat_name}')
        response.add_header('name', chat_name)  # Формируем ответ
        for chat_member in server_obj.chat_controller.get_list_users(chat_name):  # Рассылка другим пользователям
            chat_member.send_message(response)
        return response  # результат работы
    except (ChatNotFound, UserAlreadyInChat) as e:
        return Response(code=e.code, action=message.action, body=e.text)
