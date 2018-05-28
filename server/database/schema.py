from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    account_name = Column(String, unique=True)
    password = Column(String)
    avatar_path = Column(String)

    def __init__(self, account_name, password):
        self.account_name = account_name
        self.password = password

    def __repr__(self):
        return self.account_name


class UserMessage(Base):
    """
    Сообщения.
    для хранения истории
    """
    __tablename__ = 'user_messages'
    id = Column(Integer, primary_key=True)
    from_ = Column(Integer, ForeignKey('users.id'))  # от кого
    to_ = Column(Integer, ForeignKey('users.id'))  # кому
    time_ = Column(DateTime)  # дата отправки
    text_ = Column(Text)  # тело сообщения
    is_delivered = Column(Boolean)  # доставлено или нет (для оффлайн сообщений =False)

    def __init__(self, from_, to_, time_, text_, is_delivered):
        self.from_ = from_
        self.to_ = to_
        self.time_ = time_
        self.text_ = text_
        self.is_delivered = is_delivered

    def __repr__(self):
        msg = f'User Message ' \
              f'time:{self.time_}, ' \
              f'from:{self.from_}, ' \
              f'to{self.to_}, ' \
              f'message:{self.text_}, ' \
              f'delivered:{self.is_delivered}'
        return msg


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    contact_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, user_id, contact_id):
        self.user_id = user_id
        self.contact_id = contact_id


# путь до папки где лежит этот модуль
DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь до файла базы данных
DB_PATH = os.path.join(DB_FOLDER_PATH, 'server.sqlite')
# создаем движок
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False, )  # connect_args={'check_same_thread': False})

# Не забываем создать структуру базы данных
Base.metadata.create_all(engine)
# Создаем сессию для работы
Session = sessionmaker(bind=engine)
session = Session()
