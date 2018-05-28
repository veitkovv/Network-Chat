from collections import deque


class User:
    """Класс пользователя на сервере"""

    def __init__(self, sock):
        self.account_name = 'Anonymous'
        self.sock = sock
        self.requests = deque()

    def __repr__(self):
        return f'User Object: {self.account_name} : {self.sock}'

    def set_account_name(self, account_name):
        self.account_name = account_name

    def append_request(self, msg):
        self.requests.append(msg)
