import hashlib
from server.settings import ENCODING, SALT


def get_hash(clear_text):
    """Получает хэш sha256 из строки. Используется для проверки пароля"""
    bytes_text = clear_text.encode(ENCODING)
    hash_text = hashlib.pbkdf2_hmac('sha256', bytes_text, SALT, 100000)
    return hash_text
