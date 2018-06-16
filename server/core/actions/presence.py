from server.database.db_utils import Repo
from server.database.schema import session
from server.descriptors import AccountName
from server.core.exceptions import UserNameIncorrect, UserNotFoundInDatabase
from protocol.server import Response
from protocol.codes import *
from protocol.settings import ACCOUNT_NAME_PATTERN
import re

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
    account_name_attr = AccountName()  # для валидации имени пользователя импользуем дескриптор
    try:
        account_name_attr.name = message.body  # проверяем валидность
        db.client_exists(message.body)  # ищем в базе
        return Response(code=OK, action=message.action, body=f'User {message.body} successfully found! Wow')
    except (UserNameIncorrect, UserNotFoundInDatabase) as e:
        return Response(code=e.code, action=message.action, body=e.text)

    # elif not client_exists:
    #     return Response(code=NOT_FOUND, action=message.action, body=f'User "{message.body}" not found in database')
    # elif client_exists:
    #     return Response(code=OK, action=message.action, body=f'User {message.body} found!')
    # else:
    #     return Response(code=SERVER_ERROR, action=message.action, body=f'Internal server error. message: {message}')
