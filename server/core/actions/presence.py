from server.database.db_utils import Repo
from server.database.schema import session
from server.core.exceptions import UserNameIncorrect, UserNotFoundInDatabase
from protocol.server import Response
from protocol.codes import *

db = Repo(session)


def presence_processing(server_obj, message):
    """
    Отправляется клиентом при подключении к серверу, содержит имя учетной записи.
    Ответ сервера:
    400 - имя учетной записи отсутствует или некорректно
    404 если клиент не найден в БД,
    500 - ошибка сервера
    :param message: Объект Request
    :param server_obj: объект Server
    :return: Объект Response
    """
    try:
        server_obj.user.set_account_name(message.body)  # проверяем валидность
        db.client_exists(message.body)  # ищем в базе
        return Response(code=OK, action=message.action, body=f'User {message.body} successfully found! Wow')
    except (UserNameIncorrect, UserNotFoundInDatabase) as e:
        return Response(code=e.code, action=message.action, body=e.text)
