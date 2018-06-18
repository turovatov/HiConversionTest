from sqlalchemy import Column, String, Integer

from db.base import Base


class InvitationTable(Base):
    """
    Таблица инвайтов
    """
    __tablename__ = 'invitation'

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer)
    email = Column(String, nullable=False)
    token = Column(String, nullable=False, unique=True)
