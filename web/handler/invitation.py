from flask import request, redirect, make_response

from tool.token import token_mgr
from tool.config import config_mgr
from web.handler.base import BaseRouteHandler


class InvitationHandler(BaseRouteHandler):
    """
    Обработчик запросов по инвайтам
    """

    def send(self):
        """
        Обработчик на отправку инвайта

        Проверка условий:

        1. Аутентификация
            1.1 Пришел ключ сессии в кукис.
                * Если нет, то редиректим на аутентификации.

            1.2 Ключ сессии есть в БД. То есть есть активная сессия.
                * Если нет, чистим сессию в кукис и редиректим на аутентификацию.

        2. Почта
            2.1 Email отсутствует среди уже зарегистрированных пользователей.
                То есть у нас есть запись с этой почтой в таблице инвайтов,
                Но в таблице пользователей нет ссылки на этот инвайт.
                * Если нет, то возвращаем оповещение.

            2.2 Если на email уже отправлялся инвайт, и он еще не активен,
                то в бд мы токен переписываем. Новую запись в бд при этом не создаем.
                Это даст нам возможность "деактивировать" прошлый инвайт на эту почту.

        3. Токен
            3.1 Генерируем токен, и проверяем что такой токен уникален.
                Хотя для этого используется ограничение уникальности в колонке в БД,
                И sha1 хэширование со случайной величиной, все же проверим для надежности.
                * Если попали на "совпадение", генерируем новый токен.

        Делаем запись в БД с новым инвайтом

        Высылаем письмо на указанный почтовый ящик
        * В режиме отладки пишем данные в консоль

        :return:
        """
        session_id = request.cookies.get('SESSIONID')
        if not session_id:
            return '', 401

        session = self.get_session_by(session_id=session_id)
        if not session:
            return '', 401

        user = self.get_user_by(_id=session.get('user_id'))

        token = token_mgr.generate_email_token()
        while self.get_invite_by(token=token):
            token = token_mgr.generate_email_token()

        email = request.get_json().get('email')
        url = self.get_invite_url(token=token)

        inv = self.get_invite_by(email=email)
        if inv:
            if self.get_user_by(invite_id=inv.get('id')):
                return 'Email was previously registered', 200

            self.update_invite(
                _id=inv.get('id'),
                lead_id=user.get('id'),
                token=token
            )
        else:
            self.add_invite(
                lead_id=user.get('id'),
                email=email,
                token=token
            )

        values = dict(
            href=url,
            name=user.get('login')
        )

        if config_mgr.get_debug():
            print('*' * 50)
            print('Email: {}'.format(email))
            print('URL: {}'.format(values.get('href')))
            print('*' * 50)
        else:
            from mail.sender import mail_sender
            mail_sender.send_invite_mail(email_to=email, values=values)

        return '', 200

    def apply(self, token: str):
        """
        Обработчик на Применение инвайта

        Проверка условий:

        1. Инвайт
            1.1 Токен инвайта присутствует в БД
                * Если нет, то открываем главную страницу

            1.2 Инвайт еще не был "активирован".
                Отсутствует его привязка к одному из пользователей
                * Если нет, то открываем главную страницую

        :param token: Токен инвайта
        :return:
        """
        inv = self.get_invite_by(token=token)
        if not inv:
            return redirect('/')

        if self.get_user_by(invite_id=inv.get('id')):
            return redirect('/')

        return redirect('#apply/' + token)

    @staticmethod
    def get_invite_url(token: str) -> str:
        """
        Сформируем URL инвайта
        :return:
        """
        return request.host_url + 'apply_invite/' + token
