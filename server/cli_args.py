import ipaddress
import argparse
from server.settings import HOST, PORT
from server.descriptors import Port


class GetHostAndPort:
    port = Port()  # Дескриптор для валидации порта

    def __init__(self):
        self.host = HOST
        self.port = PORT

    def get_cli_params(self):
        """
        Обработчик параметров скрипта
        -a = IP адрес
        -p = Порт
        Проверяет корректность, если чего-то не хватает то берет значения по умолчанию из settings
        :return: кортеж (IP, port) для сокета
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', type=ipaddress.IPv4Address,
                            default=HOST,
                            help=f'IPv4 адрес, по умолчанию: {HOST}')
        parser.add_argument('-p', type=int,
                            default=PORT,
                            help=f'TCP порт. Значение по умолчанию: {PORT}')
        args = parser.parse_args()
        self.host = str(args.a)  # IP адрес в строку, чтобы добавить в результат
        self.port = args.p
