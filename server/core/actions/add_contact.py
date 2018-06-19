from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response
from server.core.exceptions import ContactAlreadyExists, UserNotFoundInDatabase
from protocol.codes import OK

db = Repo(session)


def add_contact_processing(server_obj, message):
    """
    # Добавление контакта. запрос содержит имя клиента, имя контакта.
    # Ответ сервера:
    # 200 - контакт добавлен
    # 400 - имя клиента или контакта отсутствует или некорректно
    # 409 - контакт уже есть в списке.
    """
    user = server_obj.user.get_account_name
    contact = message.body
    try:
        db.add_contact(user, contact)
        return Response(code=OK, action=message.action, body=f'Contact {contact} was successfully added to contact list')
    except (ContactAlreadyExists, UserNotFoundInDatabase) as e:
        return Response(code=e.code, action=message.action, body=e.text)
