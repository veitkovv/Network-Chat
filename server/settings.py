BUFFER_SIZE = 1024
HOST = '127.0.0.1'
PORT = 7777
CLIENTS_NUM = 10
TIMEOUT = 0.1
ENCODING = 'utf-8'

# Первые size_num символов в сообщении будут отданы под размер сообщения.
# Это нужно для избежания склеивания сообщения
MESSAGE_SIZE_NUM = 4
ACCOUNT_NAME_PATTERN = '^[A-Za-z0-9]+$'
SALT = b'1pvfwm|q[wOR'
