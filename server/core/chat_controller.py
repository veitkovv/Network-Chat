from protocol.metaclass import Singleton
from server.settings import DEFAULT_CHAT
from server.core.exceptions import ChatNotFound, UserAlreadyInChat


class ChatController(metaclass=Singleton):
    def __init__(self):
        self._chats = dict()  # {name: [user1, user2]}
        self._chats.update({DEFAULT_CHAT: []})  # создаем чат all , где будут все пользователи

    def create_chat(self, chat_name):
        # if not chat_name.startswith('#'):
        #     chat_name = f'#{chat_name}'
        self._chats.update({chat_name: []})

    def destroy_chat(self, chat_name):
        self._chats.pop(chat_name)

    def add_user_to_chat(self, account_name, chat_name=DEFAULT_CHAT):
        """
        200 - успешное присоединение к чату
        400 - имя клиента или имя чата некорректно
        404 - чат не найден
        409 - пользователь уже в чате
        500 - ошибка сервера
        :param account_name:
        :param chat_name:
        """
        if chat_name not in self.get_list_chats:
            raise ChatNotFound(f'Chat "{chat_name}" does not exists.')
        elif account_name in self.get_list_users(chat_name):
            raise UserAlreadyInChat(f'User "{account_name}" already in chat "{chat_name}".')
        else:
            self._chats[chat_name].append(account_name)

    def delete_user_from_chat(self, user, chat_name=DEFAULT_CHAT):
        self._chats[chat_name].remove(user)

    def get_list_users(self, chat):
        return self._chats[chat]

    @property
    def get_list_chats(self):
        return self._chats.keys()
