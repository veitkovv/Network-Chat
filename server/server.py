from collections import deque
from threading import Thread
from server.metaclasses import Singleton
from server.settings import *
from protocol.server import Request
from server.actions import actions as actions


class Server(Thread):
    def __init__(self, sock):
        super().__init__()
        self._sock = sock
        self._queue = ReadQueue(self._sock)  # экземпляр очереди на чтение

    def read_requests(self):
        """Забирает из очереди ссообщение, определяет action, отправляет на обработку"""
        try:
            message = Request(self._queue.get_next_message)
            actions[message.action](message)
        except KeyError:
            print('action do not allowed')
            # TODO send 500 error
        except IndexError:
            # print('Empty Queue')
            pass

    def write_responses(self):
        pass

    def run(self):
        while True:
            self.read_requests()
            self.write_responses()


class Queue(metaclass=Singleton):
    """очередь сообщений должна быть в единственном экземпляре"""

    def __init__(self, sock):
        self._sock = sock
        self._queue = deque()

    def run(self):
        pass


class ReadQueue(Queue, Thread):
    def run(self):
        """Метод читает из сокета, и складывает в очередь байт-сообщения для обработки"""
        while True:
            data = self._sock.recv(BUFFER_SIZE)
            if data:
                for single_message in self.pick_messages_from_stream(data):
                    self._queue.append(single_message)

    @staticmethod
    def pick_messages_from_stream(raw_bytes):
        """
        Метод определяет размер сообщения, и из байтовой строки возвращает по одному сообщению
        TCP протокол может склеить данные, тогда json не получится
        """
        # Первые size_num символов в сообщении будут отданы под размер сообщения.
        # Это нужно для избежания склеивания сообщения
        while raw_bytes:
            # Определим размер сообщения
            message_size = int(raw_bytes[:MESSAGE_SIZE_NUM])
            # Выберем из строки сообщение
            single_message = raw_bytes[MESSAGE_SIZE_NUM:message_size + MESSAGE_SIZE_NUM]
            # Отделим наше сообщение от сырой строки, на случай если сообщений больше одного
            raw_bytes = raw_bytes[message_size + MESSAGE_SIZE_NUM:]
            yield single_message

    @property
    def get_next_message(self):
        return self._queue.popleft()
