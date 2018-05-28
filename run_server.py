from server.cli_args import GetHostAndPort
from server.listener import socket_bind
from server.server import Server

if __name__ == '__main__':
    """
    1. Получаем параметры с cli - хост порт (-a -p)
    2. Создаем сокет
    3. Создаем сервер
    """
    cli_args = GetHostAndPort()
    cli_args.get_cli_params()
    host = cli_args.host
    port = cli_args.port
    sock = socket_bind(host, port)

    server = Server(sock)
    server.mainloop()
