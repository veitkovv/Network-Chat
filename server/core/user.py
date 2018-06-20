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

    def set_account_name(self, account_name):
        self._account_name = account_name

    @property
    def get_account_name(self):
        return self._account_name

    def set_transport(self, transport):
        self._transport = transport

    @property
    def get_transport(self):
        return self._transport

    def authenticate(self):
        """Метод вызывается при успешной авторизации."""
        self._user_authenticated = True

    @property
    def is_authenticated(self):
        return self._user_authenticated

    def send_message(self, message):
        """
        Дописывает в начало длинну сообщения, и затем отправляет
        :param message - объект Response
        """
        print(f'Sending {message} to {self.get_account_name}')
        ciphered_message_with_len = append_message_len_to_message(message.to_cipher_bytes(self.aes))
        self.get_transport.write(ciphered_message_with_len)
