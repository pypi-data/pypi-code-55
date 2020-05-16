from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import os
import sys
sys.path.append('../')
from soc_settings.config import *
import datetime


# Класс - база данных клиента
class ClientDBase:
    # Класс - отображение таблицы известных пользователей
    class KnownUsers:
        def __init__(self, user):
            self.id = None
            self.username = user

    # Класс - отображение таблицы истории сообщений
    class MessageHistory:
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    # Класс - отображение списка контактов
    class Contacts:
        def __init__(self, contact):
            self.id = None
            self.name = contact

    # Конструктор класса
    def __init__(self, name):
        # Создаем движок БД, поскольку каждый клиент должен иметь свою БД
        # Поскольку клиент мультипоточный необходимо отключить проверки на подключение с разных потоков
        # иначе ошибка sqlite3.ProgrammingError
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client_{name}.db3'
        self.database_engine = create_engine(f'sqlite:///{os.path.join(path, filename)}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        # Создаем объект MetaData
        self.metadata = MetaData()

        # Создаем теблицу известных пользователей
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )

        # Создаем таблицу истории сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        # Создаем таблицу контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        # Создаем таблицы
        self.metadata.create_all(self.database_engine)

        # Создаем отображения
        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        # Создаем сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Очищаем таблицу контактов, т.к. при запуске они загрузятся с сервера
        self.session.query(self.Contacts).delete()
        self.session.commit()

    # Функция добавления контактов
    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()
    # Функция очистки контактов
    def contacts_clear(self):
        self.session.query(self.Contacts).delete()

    # Функция удаления контактов
    def del_contact(self, contact):
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    # Функция добавления известных пользователей
    # Пользователи добавляются только с сервера, поэтому таблица очищается
    def add_users(self, users_list):
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    # Функция сохраняющая сообщения
    def save_message(self, contact, direction, message):
        message_row = self.MessageHistory(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    # Функция возвращающая контакты
    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    # Функция возвращающая список известных пользователей
    def get_users(self):
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    # Функция проверяющая наличие пользователя в известных пользователях
    def check_user(self, user):
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    # Функция проверяющая наличие пользователя в контактах
    def check_contact(self, contact):
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    # Функция возвращающая историю переписки
    def get_history(self, contact):
        query = self.session.query(self.MessageHistory).filter_by(contact=contact)
        return [(history_row.contact, history_row.direction, history_row.message, history_row.date)
                for history_row in query.all()]


# отладка
if __name__ == '__main__':
    test_db = ClientDBase('test1')
    # for i in ['test3', 'test4', 'test5']:
    #     test_db.add_contact(i)
    # test_db.add_contact('test4')
    # test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    # test_db.save_message('test1', 'test2', f'Привет, я тестовое сообщение от {datetime.datetime.now()}')
    # test_db.save_message('test2', 'test1', f'Привет, я тестовое сообщение от {datetime.datetime.now()}')
    # print(test_db.get_contacts())
    # print(test_db.get_users())
    # print(test_db.check_user('test1'))
    # print(test_db.check_user('test10'))
    print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))
    # test_db.del_contact('test4')
    # print(test_db.get_contacts())
