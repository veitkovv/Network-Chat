from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response
from server.core.exceptions import NoContactsYet
from protocol.codes import IMPORTANT_NOTICE, OK

db = Repo(session)


def get_contact_processing(server_obj, message):
    """
    # Запрос на получение списка контактов. запрос содержит имя клиента
    # Ответ сервера:
    # 200 - Запрос обработан успешно
    # 101 - контакт, количество и номер контакта
    # 404 - нет контактов
    """
    user = server_obj.user.get_account_name
    try:
        contacts = db.get_contacts(user)
        contacts_count = len(contacts)
        for contact in contacts:
            contact_response = Response(code=IMPORTANT_NOTICE, action=message.action, body=contact.account_name)
            contact_response.add_header('quantity', contacts_count)
            contacts_count -= 1
            server_obj.user.send_message(contact_response)
        return Response(code=OK, action=message.action, body=f'Contact list were send to {user}')
    except (NoContactsYet,) as e:
        return Response(code=e.code, action=message.action, body=e.text)
