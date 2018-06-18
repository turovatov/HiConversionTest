from sqlalchemy import Column, String, Integer
from sqlalchemy.schema import ForeignKey

from db.base import Base


class SessionTable(Base):
    """
    Таблица активных сессий
    """
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(String, nullable=False)
