from server.database.db_utils import Repo
from server.database.schema import session
from protocol.server import Response


def presence_handle(message, user):
    db = Repo(session)
    if db.client_exists(message.body):
        unauthorized_response = Response(code=401, action=message.action,
                                         body=f'Учетная запись {message.body} не авторизована')
        user.sock.send(unauthorized_response.to_bytes())
    else:
        user_not_found = Response(code=404, action=message.action,
                                  body=f'Учетная запись {message.body} не зарегистрирована на сервере')
        user.sock.send(user_not_found.to_bytes())
