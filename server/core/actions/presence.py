from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response
from protocol.codes import *
from protocol.settings import ACCOUNT_NAME_PATTERN
import re

db = Repo(session)


def presence_processing(message):
    """
    Отправляется клиентом при подключении к серверу, содержит имя учетной записи.
    Ответ сервера:
    400 - имя учетной записи отсутствует или некорректно
    404 если клиент не найден в БД,
    500 - ошибка сервера
    :param message: Объект Request
    :return: Объект Response
    """
    client_exists = db.client_exists(message.body)
    if not message.body or not re.match(ACCOUNT_NAME_PATTERN, message.body):
        return Response(code=WRONG_REQUEST, action=message.action, body=f'Account name "{message.body}" is incorrect')
    elif not client_exists:
        return Response(code=NOT_FOUND, action=message.action, body=f'User "{message.body}" not found in database')
    elif client_exists:
        return Response(code=OK, action=message.action, body=f'User {message.body} found!')
    else:
        return Response(code=SERVER_ERROR, action=message.action, body=f'Internal server error. message: {message}')
