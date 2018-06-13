from protocol.metaclass import Singleton
from server.settings import DEFAULT_CHAT


class ChatController(metaclass=Singleton):
    def __init__(self):
        self._chats = dict()  # {name: [user1, user2]}
        self._chats.update({DEFAULT_CHAT: []})  # создаем чат #all , где будут все пользователи

    def create_chat(self, chat_name):
        if not chat_name.startswith('#'):
            chat_name = f'#{chat_name}'
        self._chats.update({chat_name: []})

    def destroy_chat(self, chat_name):
        self._chats.pop(chat_name)

    def add_user_to_chat(self, chat_name, user):
        self._chats[chat_name].append(user)

    def delete_user_from_chat(self, chat_name, user):
        self._chats[chat_name].remove(user)

    def get_list_users(self, chat):
        return self._chats[chat]

    @property
    def get_list_chats(self):
        return self._chats.keys()
