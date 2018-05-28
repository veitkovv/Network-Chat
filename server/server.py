import select
import threading
from server.settings import *
from protocol.server import Request, Response
from server.actions import actions
from server.user import User


class Server:
    def __init__(self, sock):
        super().__init__()
        self._sock = sock
        self.connected_users = list()

    @staticmethod
    def pick_messages_from_stream(raw_bytes):
        """
        Метод определяет размер сообщения, и из байтовой строки возвращает по одному сообщению
        TCP протокол может склеить данные
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

    def lookup_user_by_sock(self, sock):
        """Объект User по сокету"""
        for user in self.connected_users:
            if user.sock == sock:
                return user

    def read_requests(self, ready_to_read):
        for sock in ready_to_read:
            user = self.lookup_user_by_sock(sock)
            print(user)
            data = sock.recv(BUFFER_SIZE)
            if data:
                for single_message in self.pick_messages_from_stream(data):
                    user.append_request(single_message)

    def write_responses(self, ready_to_write):
        """Забирает из очереди ссообщение, определяет action, отправляет на обработку"""
        for sock in ready_to_write:
            user = self.lookup_user_by_sock(sock)
            if user is not None:
                if user.requests:
                    message = Request(user.requests.popleft())
                    try:
                        actions[message.action](message)
                    except KeyError:
                        error_message = Response(code=500, action=message.action, body='Action do not allowed')
                        user.sock.send(error_message.to_bytes())

    def mainloop(self):
        while True:
            try:
                sock, addr = self._sock.accept()
                print('Accepting {}:{}'.format(sock, addr))
                # пока клиент не ввел свои данные, записывается как безымянный
                new_user = User(sock)
                self.connected_users.append(new_user)
            except OSError:
                # server timeout
                pass
            finally:
                ready_to_read = []
                ready_to_write = []
                try:
                    # Для select нужен список
                    conn_list = [user.sock for user in self.connected_users]
                    ready_to_read, ready_to_write, _ = select.select(conn_list, conn_list, [])
                except (OSError, BrokenPipeError):
                    pass
                self.read_requests(ready_to_read)
                self.write_responses(ready_to_write)
