from server.database.db_utils import Repo
from server.database.schema import session
from server.core.exceptions import UserNameIncorrect, UserAlreadyInDatabase
from protocol.server import Response
from protocol.codes import CREATED

db = Repo(session)


def registration_processing(server_obj, message):
    """
    Отправляется клиентом при регистрации. содержит имя учетной записи и хеш пароля.
    Ответ сервера:
    201 - успешная регистрация
    409 - пользователь уже зарегистрирован
    400 - имя или пароль отсутствует или некорректно
    500 - ошибка сервера
    :param message: Объект Request
    :param server_obj: объект Server
    :return: Объект Response
    """
    account_name, hash_password = message.body
    try:
        server_obj.user.account_name = account_name  # проверяем валидность через дескриптор
        db.add_user(account_name, hash_password)
        return Response(code=CREATED, action=message.action, body=f'User {account_name} registration success!')
    except (UserNameIncorrect, UserAlreadyInDatabase) as e:
        return Response(code=e.code, action=message.action, body=e.text)
