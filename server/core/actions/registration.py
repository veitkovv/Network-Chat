from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response
from protocol.codes import WRONG_REQUEST, CONFLICT, CREATED
from server.database.errors import ContactAlreadyInDatabase

db = Repo(session)


def registration_processing(message):
    """
    Отправляется клиентом при регистрации. содержит имя учетной записи и хеш пароля.
    Ответ сервера:
    201 - успешная регистрация
    409 - пользователь уже зарегистрирован
    400 - имя или пароль отсутствует или некорректно
    500 - ошибка сервера
    :param message: Объект Request
    :return: Объект Response
    """
    account_name, hash_password = message.body
    if not account_name or not hash_password:
        return Response(code=WRONG_REQUEST, action=message.action,
                        body=f'Account Name "{account_name}" or password incorrect')
    elif db.client_exists(account_name):
        return Response(code=CONFLICT, action=message.action, body=f'User {account_name} already exists')
    else:
        try:
            db.add_user(account_name, hash_password)
            return Response(code=CREATED, action=message.action, body=f'User {account_name} registration success!')
        except ContactAlreadyInDatabase:
            return Response(code=CONFLICT, action=message.action, body=f'User {account_name} already exists in db')
