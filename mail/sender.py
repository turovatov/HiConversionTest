from mail.context.smtp import mail_server
from mail.factory.invite import InviteMailFactory


class MailSender(object):
    """
    Почтальон
    """

    @staticmethod
    def send_invite_mail(email_to: str, values: dict) -> bool:
        """
        Отправить письмо с приглосом
        :param email_to: Адресат
        :param values: Значения для формирования письма
        :return:
        """
        with mail_server as ms:
            kw = dict(email_to=email_to, values=values)
            mail = InviteMailFactory().create_mail(**kw)
            err = ms.send(email_to, mail)
            return not bool(err)


mail_sender = MailSender()
