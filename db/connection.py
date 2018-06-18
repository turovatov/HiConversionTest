from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.base import Base
from db.table.invitation import InvitationTable
from db.table.session import SessionTable
from db.table.user import UserTable
from tool.config import config_mgr


class DatabaseConnectionManager(object):
    """
    Менеджер для работы с БД
    """

    def __init__(self):
        self.engine = None
        self.session = None

    @contextmanager
    def session_scope(self):
        """
        Контекст для работы с бд в транзакции
        :return:
        """
        self.session = Session(self.engine)
        try:
            yield self.session
            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            raise exc
        finally:
            self.session.close()
            self.session = None

    def init_engine(self):
        """
        Подключаемся к Датабазе
        :return: Клиент для работы с БД
        """
        url = self.get_connection_url()
        self.engine = create_engine(url)

    @staticmethod
    def get_connection_url() -> str:
        """
        Получаем из настроек строку для подключения к БД
        :return:
        """
        config = config_mgr.get_db_values()
        return config.get('uri')

    def create_db(self) -> None:
        """
        Создать отсутствующие таблицы
        :return:
        """
        with self.session_scope():
            Base.metadata.create_all(self.engine)

    def init_values(self):
        """
        Инициировать первичные данные в таблицах
        Исполняем код в DEBUG-режиме
        :return:
        """
        with self.session_scope() as session:
            session.query(InvitationTable).delete()
            session.query(SessionTable).delete()
            session.query(UserTable).delete()

            session.flush()

            params = self.get_demo_user_values()
            user_row = UserTable(**params)
            session.add(user_row)
            session.flush()

            params = self.get_demo_invite_values(user_id=user_row.id)
            invite_row = InvitationTable(**params)
            session.add(invite_row)
            session.flush()

    @staticmethod
    def get_demo_user_values() -> dict:
        """
        Данные для демо-пользователя
        :return:
        """
        return dict(
            login='demo',
            password='demo',
            invite_id=None
        )

    @staticmethod
    def get_demo_invite_values(user_id: int) -> dict:
        """
        Данные для инвайта демо-пользователя
        :param user_id: Ссылка на ИД демо пользователя
        :return:
        """
        return dict(
            lead_id=user_id,
            email='demo@demo.ru',
            token='ec539a6d9b6777c36cf2e213180408b9a4d6b1d4'
        )


db_mgr = DatabaseConnectionManager()
