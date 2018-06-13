import select
from threading import Thread
from server.settings import BUFFER_SIZE
from protocol.byte_stream_handler import pick_messages_from_stream
from server.core.user import User
from server.core.handler import handle_input_message
from server.core.chat import Chat


class ServerManager:
    def __init__(self, sock, input_queue, output_queue):
        self._sock = sock
        self._input_queue = input_queue
        self._output_queue = output_queue # (user, message)
        self._default_chat = Chat(name='all')  # При инициализации создается глобальный чат #all
        self._chats = list()
        self._chats.append(self._default_chat)

    def lookup_user_by_sock(self, sock):
        """Объект User по сокету"""
        for user in self._default_chat._members.keys():
            if user.sock == sock:
                return user

    def read_requests(self, ready_to_read):
        for sock in ready_to_read:
            # Находим объект юзера
            user = self.lookup_user_by_sock(sock)
            try:
                data = sock.recv(BUFFER_SIZE)
                if data:
                    # Добавляем в очередь входящих кортеж (User, Data)
                    for single_message in pick_messages_from_stream(data):
                        self._input_queue.append((user, single_message))
            except ConnectionError:
                self._default_chat._members.pop(user)
                print(f'User {user.account_name} was disconnected from the server')

    def handle_requests(self):
        print('input message handler started')
        while True:
            if self._input_queue:
                message = self._input_queue.popleft()
                handle_input_message(message)

    def write_responses(self, ready_to_write):
        if self._output_queue:
            user, message = self._output_queue.popleft()
            if user.sock in ready_to_write:
                user.sock.send(message)

    def mainloop(self):
        while True:
            try:
                sock, addr = self._sock.accept()
                print(f'Accepting {sock}:{addr}')
                # пока клиент не ввел свои данные, записывается как безымянный
                new_user = User(sock)
                self._default_chat.add_member(new_user)

            except OSError:
                # server timeout
                pass
            finally:
                ready_to_read = []
                ready_to_write = []
                try:
                    # Для select нужен список
                    conn_list = [user.sock for user in self._default_chat._members.keys()]
                    ready_to_read, ready_to_write, _ = select.select(conn_list, conn_list, [])
                except (OSError, BrokenPipeError):
                    pass
                self.read_requests(ready_to_read)
                self.write_responses(ready_to_write)

    def serve_forever(self):
        main_thread = Thread(target=self.mainloop, daemon=True)
        h_thread = Thread(target=self.handle_requests, daemon=True)
        main_thread.start()
        h_thread.start()
        main_thread.join()
        h_thread.join()
