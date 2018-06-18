import smtplib

from tool.config import config_mgr


class SmtpServerContext(object):
    """
    Контекстный менеджер для работы с SMTP-сервером
    """

    def __init__(self):
        self.server = None
        self.smtp_server = self.get_server_url()
        self.username = self.get_username()
        self.password = self.get_password()

    def __enter__(self):
        self.server = smtplib.SMTP(self.smtp_server)
        self.server.starttls()
        self.server.login(self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()

    @staticmethod
    def get_username() -> str:
        """
        Получаем из настроек имя пользователя для подключения к SMTP
        :return:
        """
        values = config_mgr.get_smtp_values()
        return values.get('username')

    @staticmethod
    def get_password() -> str:
        """
        Получаем из настроек пароль для подключения к SMTP
        :return:
        """
        values = config_mgr.get_smtp_values()
        return values.get('password')

    @staticmethod
    def get_server_url() -> str:
        """
        Получаем из настроек сетевой адрес для подключения к SMTP
        :return:
        """
        values = config_mgr.get_smtp_values()
        return values.get('server')

    def send(self, email_to: str, mail: str) -> dict:
        """
        Осуществляем физическую отправку письма через сервер
        :param email_to: Адрес почты
        :param mail: Текстовое письмо
        :return:
        """
        from_to = self.username
        err = self.server.sendmail(from_to, email_to, mail)
        print(err)
        return err


mail_server = SmtpServerContext()
