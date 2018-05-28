import socket
import threading
from client.cli_args import GetHostAndPort
from client.settings import BUFFER_SIZE, ENCODING
from client.actions import Sender


class Client:
    cli_args = GetHostAndPort()
    cli_args.get_cli_params()

    def __init__(self):
        # Создаем экземпляр сокет соединения
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Связываем сокет соединение с хостом и портом сервера
        self._sock.connect((self.cli_args.host, self.cli_args.port))
        self._sender = Sender(self._sock)

    @staticmethod
    def read(sock):
        while True:
            # Получаем данные с сервера
            bytes_data = sock.recv(BUFFER_SIZE)
            # Приводим полученные данные к строковому виду
            str_data = bytes_data.decode(ENCODING)
            # Выводим полученные данные на экран
            print(str_data)

    def write(self):
        while True:
            # Вводим данные с клавиатуры
            str_data = input('Enter data: ')
            self._sender.msg(str_data, '#all')

    def send(self):
        while True:
            self._sender.send_next_message()

    def run(self):
        reader_thread = threading.Thread(target=self.read, args=(self._sock,))
        writer_thread = threading.Thread(target=self.write)
        sender_thread = threading.Thread(target=self.send)
        sender_thread.daemon = True

        try:
            reader_thread.start()
            writer_thread.start()
            sender_thread.start()
        except KeyboardInterrupt:
            # Обрабатываем сочетание клавиш Ctrl+C
            pass
