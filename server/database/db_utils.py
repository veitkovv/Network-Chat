from server.database.schema import User, Contact, UserMessage
from server.core.exceptions import (UserNotFoundInDatabase, UserAlreadyInDatabase, ContactAlreadyExists,
                                    ContactDoesNotExist)
import datetime


class Repo:
    def __init__(self, session):
        self._session = session

    def add_user(self, user_name, hash_password):
        try:
            self.client_exists(user_name)
        except UserNotFoundInDatabase:
            new_user = User(user_name, hash_password)
            self._session.add(new_user)
            self._session.commit()
        else:
            raise UserAlreadyInDatabase(f'User "{user_name}" already registered on the server')

    def client_exists(self, user_name):
        result = self._session.query(User).filter(User.account_name == user_name).count() > 0
        if not result:
            raise UserNotFoundInDatabase(f'User "{user_name}" is not found in database')
        else:
            return result

    def contact_exists(self, user_name, contact_name):
        """Проверка, есть ли контакт"""
        user = self.get_client_by_username(user_name)
        contact = self.get_client_by_username(contact_name)
        result = self._session.query(Contact).filter(Contact.user_id == user.id).filter(
            Contact.contact_id == contact.id).count() > 0
        return result

    def get_client_by_username(self, account_name):
        """Получение клиента по имени"""
        if self.client_exists(account_name):
            client = self._session.query(User).filter(User.account_name == account_name).first()
            return client

    def get_client_username_by_id(self, user_id):
        """Имя клиента по id"""
        client = self._session.query(User.account_name).filter(User.id == user_id).first()
        return str(client[0])  # результат преобразовываем в строку

    def add_contact(self, client_username, contact_username):
        """Добавление контакта"""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                if not self.contact_exists(client_username, contact_username):
                    client_contact = Contact(user_id=client.id, contact_id=contact.id)
                    self._session.add(client_contact)
                    self._session.commit()
                else:
                    raise ContactAlreadyExists(f'Contact {contact_username} already in contact list')
            else:
                raise UserNotFoundInDatabase(f'Error! User {client_username} not found')
        else:
            raise UserNotFoundInDatabase(f'User {contact_username} does not registered on this server')

    def del_contact(self, client_username, contact_username):
        """Удаление контакта"""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                if self.contact_exists(client_username, contact_username):
                    cc = self._session.query(Contact).filter(
                        Contact.user_id == client.id).filter(
                        Contact.contact_id == contact.id).first()
                    self._session.delete(cc)
                    self._session.commit()
                else:
                    raise ContactDoesNotExist(f'Contact {contact_username} not in contact list')
            else:
                raise UserNotFoundInDatabase(f'Error! User {client_username} not found')
        else:
            raise UserNotFoundInDatabase(f'User {contact_username} does not registered on this server')

    def get_contacts(self, client_username):
        """Получение контактов клиента"""
        client = self.get_client_by_username(client_username)
        result = []
        if client:
            # Тут нету relationship поэтому берем запросом
            contacts_clients = self._session.query(Contact).filter(Contact.user_id == client.id)
            for contact_client in contacts_clients:
                contact = self._session.query(User).filter(User.id == contact_client.contact_id).first()
                result.append(contact)
        return result

    # def get_client_avatar(self, account_name):
    #     """
    #     Ищет в БД путь до клиентского аватара
    #     Если поле пустое - возвращает дефолтный аватар
    #     """
    #     client = self.get_client_by_username(account_name)
    #     if client.avatar_path:
    #         return client.avatar_path
    #     else:
    #         return DEFAULT_AVATAR_PATH

    # def set_client_avatar(self, account_name, path):
    #     """Записывает клиенту путь до его аватара"""
    #     client = self.get_client_by_username(account_name)
    #     client.avatar_path = path
    #     self._session.commit()

    def add_message(self, from_, to_, time_, text_, is_delivered=False):
        """Хранение личных сообщений в БД"""
        time_datetime = datetime.datetime.fromtimestamp(int(time_))  # из timestamp в datetime
        user_from = self.get_client_by_username(from_)
        user_to = self.get_client_by_username(to_)
        new_message = UserMessage(user_from.id, user_to.id, time_datetime, text_, is_delivered)
        self._session.add(new_message)
        self._session.commit()

    # def get_delayed_messages(self, account_name):
    #     """получение сообщений, которые не доставлены"""
    #     user = self.get_client_by_username(account_name)
    #     undelivered_messages = self._session.query(UserMessage).filter(UserMessage.to_ == user.id).filter(
    #         UserMessage.is_delivered == False).all()
    #     for message in undelivered_messages:
    #         receiver = self.get_client_username_by_id(message.to_)
    #         sender = self.get_client_username_by_id(message.from_)
    #         time_ = time.mktime(message.time_.timetuple())
    #         text = '[Оффлайн сообщение] {}'.format(message.text_)
    #         try:
    #             message.is_delivered = True
    #             self._session.commit()
    #             yield sender, receiver, time_, text
    #         except Exception as e:
    #             self._session.rollback()
    #             print(e)
