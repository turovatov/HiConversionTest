from db.manager.base import BaseDataManager
from db.table.session import SessionTable


class SessionManager(BaseDataManager):
    """
    Менеджер для работы с таблицей Session
    """

    table = SessionTable

    def add_(self, user_id: int, session_id: str) -> dict:
        """
        Изменить токен существующей сесии, или добавить новую сессию
        :param user_id: ID пользователя
        :param session_id: Токен сессии
        :return: Токен сессии
        """

        session = self.get_by(user_id=user_id)
        if not session:
            return self.add(user_id=user_id, session_id=session_id)
        else:
            return self.update(_id=session.get('id'), session_id=session_id)
