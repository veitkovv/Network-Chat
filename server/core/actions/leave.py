from protocol.server import Response
from protocol.codes import OK
from server.core.exceptions import NoChatNameError, UserNotAMember, DefaultChatLeaveError, ChatDoesNotExist


def leave_processing(server_obj, message):
    """
    Запрос на выход из чата. содержит имя чата (Выйти из чата #all нельзя).
    Ответ сервера:
    200 - успешный выход из чата
    409 - Пользователь не является членом чата
    :param message:
    :param server_obj:
    """
    chat_name = message.body
    try:
        server_obj.chat_controller.delete_user_from_chat(server_obj.user, chat_name)  # Удаляем пользователя из чата
        response = Response(code=OK, action=message.action,
                            body=f'User "{server_obj.user.get_account_name}" successfully leaved chat {chat_name}')
        response.add_header('name', chat_name)  # Формируем ответ
        for chat_member in server_obj.chat_controller.get_list_users(chat_name):  # Рассылка другим пользователям
            chat_member.send_message(response)
        return response  # результат работы
    except (NoChatNameError, UserNotAMember, DefaultChatLeaveError, ChatDoesNotExist) as e:
        return Response(code=e.code, action=message.action, body=e.text)
