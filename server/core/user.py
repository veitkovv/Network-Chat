from server.descriptors import AccountName
from protocol.crypto.aes import CipherAes
from protocol.byte_stream_handler import append_message_len_to_message


class User:
    """Класс пользователя на сервере"""
    _account_name = AccountName()  # проверка валидности user-name

    def __init__(self, account_name):
        self._account_name = account_name
        self._transport = None
        self.public = None  # ключ rsa публичный
        self.private = None  # ключ rsa приватный
        self.aes = CipherAes('')  # Для шифрования AES
        self._user_authenticated = False

    def __repr__(self):
        return f'User Object: {self._account_name} {self._transport}'

    @property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, value):
        self._account_name = value

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, value):
        self._transport = value

    @property
    def is_authenticated(self):
        return self._user_authenticated

    def authenticate(self):
        """Метод вызывается при успешной авторизации."""
        self._user_authenticated = True

    def send_message(self, message):
        """
        Дописывает в начало длинну сообщения, и затем отправляет
        :param message - объект Response
        """
        # print(f'Sending {message} to {self.account_name}')
        ciphered_message_with_len = append_message_len_to_message(message.to_cipher_bytes(self.aes))
        self.transport.write(ciphered_message_with_len)
