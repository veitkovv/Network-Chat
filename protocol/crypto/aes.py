from Cryptodome.Cipher import AES


class CipherAes:
    """Класс обеспечивает методы шифрования"""

    def __init__(self, secret):
        self._secret = secret

    def set_secret(self, secret):
        self._secret = secret

    @property
    def get_secret(self):
        return self._secret

    @staticmethod
    def padding_text(text):
        """
        Выравнивание сообщения до длины кратной 16 байтам.
        В данном случае исходное сообщение дополняется пробелами.
        """
        pad_len = (16 - len(text) % 16) % 16
        return text + b' ' * pad_len

    def encrypt(self, plaintext):
        """
        Шифрование сообщения plaintext ключом self._secret.
        Атрибут iv - вектор инициализации для алгоритма шифрования.
        Если не задаётся явно при создании объекта-шифра, то генерируется
        случайно.
        Его следует добавить в качестве префикса к финальному шифру,
        чтобы была возможность правильно расшифровать сообщение.
        """
        plaintext_padded = self.padding_text(plaintext)
        cipher = AES.new(self._secret, AES.MODE_CBC)
        cipher_text = cipher.iv + cipher.encrypt(plaintext_padded)
        return cipher_text

    def decrypt(self, cipher_text):
        """
        Расшифровка шифра ciphertext ключом self._secret.
        Вектор инициализации берётся из исходного шифра.
        Его длина для большинства режимов шифрования всегда 16 байт.
        Расшифровываться будет оставшаяся часть шифра.
        """
        cipher = AES.new(self._secret, AES.MODE_CBC, iv=cipher_text[:16])
        msg = cipher.decrypt(cipher_text[16:])
        return msg.strip()  # Пробелы в конце не нужны
