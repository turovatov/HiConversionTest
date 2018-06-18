from db.manager.base import BaseDataManager
from db.table.invitation import InvitationTable


class InvitationManager(BaseDataManager):
    """
    Менеджер для работы с таблицей Invitation
    """

    table = InvitationTable
