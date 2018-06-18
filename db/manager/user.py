from db.manager.base import BaseDataManager
from db.table.user import UserTable


class UserManager(BaseDataManager):
    """
    Менеджер для работы с таблицей User
    """

    table = UserTable
