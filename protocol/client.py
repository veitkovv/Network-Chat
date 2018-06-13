import json
import protocol.settings
import time


class Request:
    """Класс для составления запроса на сервер"""

    def __init__(self, action, body, **headers):
        """Конструктор в качестве аргументов принимает основные данные о запросе"""
        self._headers = headers
        self._action = action
        self._body = body

    def __repr__(self):
        return f'<action = {self._action} \n body = {self._body} \n headers = {self._headers}>'

    def add_header(self, key, value):
        """
        Метод add_header - используется для добавления дополнительных данных о запросе, например времени его совершения
        """
        self._headers.update({key: value})

    def remove_header(self, key):
        """
        Метод remove_header - используется для удаления дополнительных данных о запросе,
        если во время его заполнения была допущена ошибка
        """
        del self._headers[key]

    def make_envelope(self):
        envelope = dict()
        self.add_header('time', time.time())  # Добавим время в сообщение
        envelope.update({'action': self._action})
        envelope.update({'headers': self._headers})
        envelope.update({'body': self._body})
        return envelope

    def to_bytes(self):
        """
        Метод to_bytes - используется для преобразования данных о запросе в байты
        :return: байт-строку из JSON-строки
        """
        data_str = json.dumps(self.make_envelope())
        return data_str.encode(protocol.settings.ENCODING)

    def to_cipher_bytes(self, aes):
        return aes.encrypt(self.to_bytes())


class Response:
    """Response-объект - используется для преобразования "сырых" данных (байтов) в python-объект"""

    def __init__(self, message_bytes):
        """
        Конструктор в качестве аргументов принимает исключительно "сырые" зашифрованные данные
        Внутри конструктора "сырые" данные преобразуются в словарь
        """
        message_str = message_bytes.decode(protocol.settings.ENCODING)
        self._envelope = json.loads(message_str)

    def __repr__(self):
        return f'<{self._envelope}>'

    @property
    def code(self):
        """Read only свойство code"""
        code = self._envelope.get('code')
        return code

    @property
    def action(self):
        """Read only свойство action"""
        action = self._envelope.get('action')
        return action

    @property
    def headers(self):
        """
        Read only свойство headers
        Свойство headers содержит дополнительные данные об ответе сервера, например время его совершения
        """
        headers = self._envelope.get('headers')
        return headers

    @property
    def body(self):
        """
        Read only свойство body
        Свойство body содержит тело ответа сервера
        """
        body = self._envelope.get('body')
        return body
