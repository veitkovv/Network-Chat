BUFFER_SIZE = 1024
HOST = '127.0.0.1'
PORT = 7777
ENCODING = 'utf-8'

ACCOUNT_NAME_PATTERN = '^[A-Za-z0-9]+$'
ACCOUNT_NAME_MAX_LEN = 31
DEFAULT_CHAT = '#all'
AUTHENTICATION_REQUIRED_ACTIONS = (
    'msg',
    'join',
    'leave',
    'add_contact',
    'del_contact',
    'get_contacts',
    'get_chats',
)
