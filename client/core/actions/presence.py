from protocol.client import Request
from protocol.codes import NOT_FOUND, WRONG_REQUEST, SERVER_ERROR, OK
from protocol.crypto.utils import get_hash


def presence_request(ui_instance):
    ui_instance.request_account_name('Type your account name: ')
    return Request(action='presence', body=ui_instance.account_name)


def presence_response(response_message, ui_instance):
    """Обработка ответа сервера на presence"""
    if response_message.code == OK:  # Если все хорошо, запрос на join . пустое тело = дефолтный чат.
        return Request(action='join', body='')
    elif response_message.code == NOT_FOUND:  # Если юзер не найден, регистрация
        new_password = ui_instance.request_password('Type new password: ')
        return Request(action='registration', body=[ui_instance.account_name, get_hash(new_password)])
    elif response_message.code == WRONG_REQUEST:  # Неверное имя пользователя (не формат), новый ввод
        new_account_name = ui_instance.request_account_name('Please type the correct account name: ')
        ui_instance.account_name(new_account_name)
        return Request(action='presence', body=new_account_name)
    elif response_message.code == SERVER_ERROR:
        pass  # just show the message, nothing to do
    else:
        print(f'Неизвестная ошибка! Сообщение: {response_message}')
