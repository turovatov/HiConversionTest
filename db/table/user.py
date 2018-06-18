from sqlalchemy import Column, String, Integer, ForeignKey

from db.base import Base


class UserTable(Base):
    """
    Таблица зарегистрированных пользователей
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    invite_id = Column(Integer, ForeignKey('invitation.id'), nullable=True)
