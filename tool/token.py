from hashlib import sha1
from time import time


class TokenManager(object):
    """
    Менеджер для работы генерации токенов
    """

    @staticmethod
    def generate_session_id() -> str:
        """
        Сгенерировать токен сессии
        :return:
        """
        salt = '1gz.8f8.&0u-'
        value = salt.join(str(time()))
        return sha1(value.encode()).hexdigest()

    @staticmethod
    def generate_email_token() -> str:
        """
        Сгенерировать токен для инвайта
        :return:
        """
        salt = 'woody88study'
        value = salt.join(str(time()))
        return sha1(value.encode()).hexdigest()


token_mgr = TokenManager()
