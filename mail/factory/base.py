import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mako.lookup import TemplateLookup

from tool.config import config_mgr


class BaseMailFactory(object):
    """
    Базовая фабрика для создания писем
    """

    subject = None
    template = None

    def __init__(self):
        self.from_to = self.get_from_to()

    def get_subject(self):
        """
        Прочитать значение "Тема письма".
        Если не указали, то генерируем ошибку
        :return:
        """
        if not self.subject:
            raise NotImplementedError('Mail subject is not defined')
        return self.subject

    def get_template(self):
        """
        Прочитать значение "Шаблон письма".
        Если не указали, то генерируем ошибку
        :return:
        """
        if not self.template:
            raise NotImplementedError('Mail template is not defined')
        return self.template

    @staticmethod
    def get_from_to():
        """
        Прочитать значение "От кого" из конфигурационного файла.
        Если не указали, то генерируем ошибку
        :return:
        """
        values = config_mgr.get_smtp_values()
        return values.get('username')

    def create_mail(self, email_to: str, values: dict) -> str:
        """
        Сформировать письмо
        :param email_to: Кому отправляем, адрес
        :param values: Данные для генерации по шаблону
        :return:
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.get_subject()
        msg['From'] = 'dmitry.turovatov@eteron.ru'
        msg['To'] = email_to

        html = self.mako_render(tmpl=self.get_template(), data=values)
        mime_html = MIMEText(html, 'html')
        msg.attach(mime_html)

        return msg.as_string()

    @staticmethod
    def get_template_folder():
        """
        Получаем папку для шабонов
        :return:
        """
        return os.getcwd() + '/mail/template/'

    def mako_render(self, tmpl: str, data: dict) -> str:
        """
        Генерируем HTML по шаблону
        :param tmpl: шаблон
        :param data: данные для генерации
        :return:
        """
        tmpl_params = dict(
            directories=[self.get_template_folder()],
            input_encoding='utf-8',
            output_encoding='utf-8'
        )
        template_lookup = TemplateLookup(**tmpl_params)
        template = template_lookup.get_template(uri=tmpl)
        html = template.render(**data)
        return html.decode()
