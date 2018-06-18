from flask import make_response, redirect

from db.manager.invitation import InvitationManager
from db.manager.session import SessionManager
from db.manager.user import UserManager


class BaseRouteHandler(object):
    """
    Базовый класс для обраточика запросов
    """

    @staticmethod
    def get_session_by(**kwargs):
        return SessionManager().get_by(**kwargs)

    @staticmethod
    def get_user_by(**kwargs):
        return UserManager().get_by(**kwargs)

    @staticmethod
    def get_invite_by(**kwargs):
        return InvitationManager().get_by(**kwargs)

    @staticmethod
    def add_user(**kwargs):
        return UserManager().add(**kwargs)

    @staticmethod
    def add_invite(**kwargs):
        return InvitationManager().add(**kwargs)

    @staticmethod
    def add_session(user_id: int, session_id: str):
        return SessionManager().add_(user_id, session_id)

    @staticmethod
    def update_invite(**kwargs):
        return InvitationManager().update(**kwargs)
