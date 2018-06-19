from protocol.metaclass import Singleton
from server.settings import DEFAULT_CHAT
from server.core.exceptions import (ChatNotFound, UserAlreadyInChat, ChatDoesNotExist, NoChatNameError, UserNotAMember,
                                    DefaultChatLeaveError)


class ChatController(metaclass=Singleton):
    def __init__(self):
        self._chats = dict()  # {name: [user1, user2]}
        self._chats.update({DEFAULT_CHAT: []})  # создаем чат all , где будут все пользователи

    def create_chat(self, chat_name):
        if not chat_name.startswith('#'):
            chat_name = f'#{chat_name}'
        self._chats.update({chat_name: []})

    def destroy_chat(self, chat_name):
        self._chats.pop(chat_name)

    def add_user_to_chat(self, user_obj, chat_name=DEFAULT_CHAT):
        """
        404 - чат не найден
        409 - пользователь уже в чате
        :param user_obj:
        :param chat_name:
        """
        if chat_name not in self.get_chats.keys():
            raise ChatNotFound(f'Chat "{chat_name}" does not exists.')
        elif user_obj in self.get_list_users(chat_name):
            raise UserAlreadyInChat(f'User "{user_obj.get_account_name}" already a member {chat_name}.')
        else:
            self._chats[chat_name].append(user_obj)

    def delete_user_from_chat(self, user_obj, chat_name):
        if not chat_name:
            raise NoChatNameError('Error! Empty Chat Name!')
        elif user_obj not in self.get_list_users(chat_name):
            raise UserNotAMember(f'User {user_obj.get_account_name} not a member of chat {chat_name}')
        elif chat_name == DEFAULT_CHAT:
            raise DefaultChatLeaveError(f'Error! You can\'t leave default chat {DEFAULT_CHAT}')
        else:
            self._chats[chat_name].remove(user_obj)

    def get_list_users(self, chat_name=DEFAULT_CHAT):
        try:
            return self._chats[chat_name]
        except KeyError:
            raise ChatDoesNotExist(f'Chat {chat_name} does not exist')

    @property
    def get_chats(self):
        return self._chats
