from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA256
from protocol.settings import ENCODING


class CipherRSA:
    pass


def generate_rsa_pair():
    random_generator = Random.new().read
    private_key = RSA.generate(2048, random_generator)
    public_key = private_key.publickey()
    return public_key, private_key


def public_key_from_bytes(bytes_key):
    return RSA.import_key(bytes_key)


def rsa_cipher_byte_string(clean_byte_string, key):
    cipher = PKCS1_OAEP.new(key)
    cipher_text = cipher.encrypt(clean_byte_string)
    return cipher_text


def rsa_decipher_byte_string(ciphered_byte_string, key):
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(ciphered_byte_string)
    return message


def get_hash(clear_text):
    """Получает хэш sha256 из строки. Используется для проверки пароля"""
    bytes_text = clear_text.encode(ENCODING)
    h = SHA256.new()
    h.update(bytes_text)
    return h.hexdigest()


def get_session_key(length):
    return Random.get_random_bytes(length)
