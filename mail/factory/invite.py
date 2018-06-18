from mail.factory.base import BaseMailFactory


class InviteMailFactory(BaseMailFactory):
    """
    Фабрика для создания письма с приглашением
    """

    subject = 'Invite To Party!!'
    template = 'invite.mako'
