from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response
from protocol.codes import WRONG_REQUEST, SERVER_ERROR, NOT_FOUND, ACCEPTED, UNAUTHORIZED
from protocol.crypto.utils import compare_hashes

db = Repo(session)


def authenticate_processing(message, user_obj):
    """
    Отправляется клиентом при авторизации. содержит имя учетной записи и хеш пароля.
    Ответ сервера:
    202 если пароль верный,
    400 - имя или пароль отсутствует или некорректно
    401 если пароль неверный,
    403 если пользователь заблокирован,
    404 если клиент не найден в БД.
    500 - ошибка сервера
    :param message: Объект Request
    :param user_obj: Объект User
    :return: Объект Response
    """
    account_name, password_hash = message.body
    server_stored_password = db.get_client_by_username(account_name).password
    if server_stored_password is None:
        return Response(code=NOT_FOUND, action=message.action, body=f'User "{account_name}" not found')
    elif not password_hash:
        return Response(code=WRONG_REQUEST, action=message.action, body='Password must be present')
    elif compare_hashes(server_stored_password, password_hash):
        user_obj.set_account_name(account_name)
        user_obj.set_authenticated()
        return Response(code=ACCEPTED, action=message.action, body=f'Authentication success! Welcome, {account_name}')
    elif not compare_hashes(server_stored_password, password_hash):
        return Response(code=UNAUTHORIZED, action=message.action, body='Wrong Password')
    else:
        return Response(code=SERVER_ERROR, action=message.action, body=f'Server Error! message: {message}')
