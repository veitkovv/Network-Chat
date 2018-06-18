from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response
from server.core.exceptions import UserNameIncorrect, UserNotFoundInDatabase, EmptyHashValue, PasswordsDidntMatch
from protocol.codes import ACCEPTED
from protocol.crypto.utils import compare_hashes

db = Repo(session)


def authenticate_processing(server_obj, message):
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
    :param server_obj: Объект server
    :return: Объект Response
    """
    account_name, password_hash = message.body
    try:
        server_obj.user.set_account_name(account_name)  # проверяем валидность имени
        server_stored_password = db.get_client_by_username(account_name).password  # ищем пароль в БД
        if compare_hashes(server_stored_password, password_hash):
            server_obj.user.authenticate()
            return Response(code=ACCEPTED, action=message.action,
                            body=f'Authentication success! Welcome, {account_name}')
    except (UserNameIncorrect, UserNotFoundInDatabase, EmptyHashValue, PasswordsDidntMatch) as e:
        return Response(code=e.code, action=message.action, body=e.text)
