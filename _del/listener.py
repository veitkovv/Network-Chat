import socket
from server.settings import CLIENTS_NUM, TIMEOUT


def socket_bind(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(CLIENTS_NUM)
    sock.settimeout(TIMEOUT)
    print('Listening {}:{}...'.format(host, port))
    return sock
