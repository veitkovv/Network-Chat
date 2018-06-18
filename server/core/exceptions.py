from protocol.codes import *


class BaseError(Exception):
    """базовая ошибка. Содержит в себе код ошибки."""

    def __init__(self, code, text=''):
        self.code = code  # Код ошибки из протокола
        self.text = text  # текст ошибки. по умолчанию - пустая строка


class ServerError(BaseError):
    def __init__(self, text):
        super().__init__(code=SERVER_ERROR)
        self.text = text


class UserNameIncorrect(BaseError):
    def __init__(self, text):
        super().__init__(code=WRONG_REQUEST)
        self.text = text


class ChatNotFound(BaseError):
    def __init__(self, text):
        super().__init__(code=NOT_FOUND)
        self.text = text


class UserAlreadyInChat(BaseError):
    def __init__(self, text):
        super().__init__(code=CONFLICT)
        self.text = text


class UserNotFoundInDatabase(BaseError):
    def __init__(self, text):
        super().__init__(code=NOT_FOUND)
        self.text = text


class EmptyHashValue(BaseError):
    def __init__(self, text):
        super().__init__(code=WRONG_REQUEST)
        self.text = text


class PasswordsDidntMatch(BaseError):
    def __init__(self, text):
        super().__init__(code=WRONG_REQUEST)
        self.text = text


class UserAlreadyInDatabase(BaseError):
    def __init__(self, text):
        super().__init__(code=CONFLICT)
        self.text = text


class ChatDoesNotExist(BaseError):
    def __init__(self, text):
        super().__init__(code=NOT_FOUND)
        self.text = text


class ContactAlreadyExists(BaseError):
    def __init__(self, text):
        super().__init__(code=CONFLICT)
        self.text = text


class ContactDoesNotExist(BaseError):
    def __init__(self, text):
        super().__init__(code=NOT_FOUND)
        self.text = text
