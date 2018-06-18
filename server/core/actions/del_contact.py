from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response
from server.core.exceptions import ContactDoesNotExist, UserNotFoundInDatabase
from protocol.codes import OK

db = Repo(session)


def del_contact_processing(server_obj, message):
    """
    # Удаление контакта. запрос содержит имя клиента, имя контакта.
    # Ответ сервера:
    # 200 - контакт удален
    # 400 - имя клиента или контакта отсутствует или некорректно
    # 409 - контакта не существует в списке.
    """
    user = server_obj.user.get_account_name
    contact = message.body
    try:
        db.del_contact(user, contact)
        return Response(code=OK, action=message.action,
                        body=f'Contact {contact} has successfully deleted from contact list')
    except (ContactDoesNotExist, UserNotFoundInDatabase) as e:
        return Response(code=e.code, action=message.action, body=e.text)
