import json
import protocol.settings
import time


class Request:
    """
    Request-объект - используется для преобразования "сырых" данных (байтов) в python-объект
    """

    def __init__(self, message_bytes):
        """
        Конструктор в качестве аргументов принимает исключительно "сырые" данные
        Внутри конструктора "сырые" данные преобразуются в словарь
        """
        message_str = message_bytes.decode(protocol.settings.ENCODING)
        self._envelope = json.loads(message_str)

    def __repr__(self):
        return f'<{self._envelope}>'

    @property
    def action(self):
        """Read only свойство action"""
        action = self._envelope.get('action')
        return action

    @property
    def headers(self):
        """
        Read only свойство headers
        Свойство headers содержит дополнительные данные о запросе, например время его совершения
        """
        headers = self._envelope.get('headers')
        return headers

    @property
    def body(self):
        """
        Read only свойство body
        Свойство body содержит тело запроса
        """
        body = self._envelope.get('body')
        return body


class Response:
    """
    Response-объект - используется для приведения python-объекта в байтовый вид (для генерации "сырых" данных)
    """

    def __init__(self, code, action, body, **headers):
        """Конструктор в качестве аргументов принимает основные данные об ответе сервера"""
        self._headers = headers
        self._action = action
        self._code = code
        self._body = body

    def __repr__(self):
        return f'<code - {self._code} : action - {self._action} : body - {self._body} : headers - {self._headers}>'

    def add_header(self, key, value):
        """
        Метод add_header - используется для добавления дополнительных данных об товете сервера,
        например времени его совершения
        """
        self._headers.update({key: value})

    def remove_header(self, key):
        """
        Метод add_header - используется для удаления дополнительных данных об товете сервера,
        если во время его заполнения была допущена ошибка
        """
        del self._headers[key]

    def get_header(self, key):
        try:
            return self._headers[key]
        except KeyError:
            return False

    def make_envelope(self):
        envelope = dict()
        self.add_header('time', time.time())  # Добавим время в сообщение
        envelope.update({'code': self._code})
        envelope.update({'action': self._action})
        envelope.update({'headers': self._headers})
        envelope.update({'body': self._body})
        return envelope

    def to_bytes(self):
        """Метод to_bytes - используется для преобразования данных об ответе сервера в байты"""
        data_str = json.dumps(self.make_envelope())
        return data_str.encode(protocol.settings.ENCODING)

    def to_cipher_bytes(self, aes):
        return aes.encrypt(self.to_bytes())
