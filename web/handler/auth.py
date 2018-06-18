from flask import request, json, redirect, make_response

from tool.token import token_mgr
from web.handler.base import BaseRouteHandler


class AuthHandler(BaseRouteHandler):
    """
    Обработчик запросов по аутентификации
    """

    def sign_in(self):
        """
        Аутентификация по учетным данным

        1.  Проверяем наличие пользователя в БД
            * Если его нет, то возвращаем ошибку аутентификации

        2. Если он есть, то создаем для него активную сессию
            Пишем ее в БД. Для хранения сессий можем использовать Redis

        3. Ключ сессии пишем в кукис.
            По нему мы будем определять пользователя при каждом запросе.
            Это очень упрощенный вариант.

        :return:
        """
        login = request.get_json().get('login')
        password = request.get_json().get('password')

        user = self.get_user_by(
            login=login,
            password=password
        )
        if not user:
            return 'User not found', 200

        new_session_id = token_mgr.generate_session_id()

        self.add_session(
            user_id=user.get('id'),
            session_id=new_session_id
        )

        response = make_response()
        response.set_cookie('SESSIONID', new_session_id)
        response.set_cookie('UID', login)
        return response

    @staticmethod
    def sign_out():
        """
        Выход из системы

        1. Чистим сессию в кукис
        2. Редиректим на аутентификацию

        :return:
        """
        return '', 401

    def sign_up(self):
        """
        Регистрация по инвайту

        1. Валидируем входные данные
            Логин, пароль, и токен инвайта - это строки
            Условий на данные не ставилось, но валидировать нужно

        2. Проверяем условия
            2.1 Наш токен есть в БД
                * Если нет, то возвращаем сообщение об ошибке

            2.2 Проверяем инвайт. Не был ли он активирован уже.
                * Если активирован, то возвращаем сообщение об ошибке

            2.3 Проверяем был ли создан такой пользователь ранее
                * Если да, то возвращаем сообщение об ошибке

        3. Создаем нового пользователя
            Привязываем к нему ссылку на инвайт

        4. Создаем новую сессию для этого пользователя.
            И пишем ее в кукис, чтобы он мог пользоваться системой

        :return:
        """

        login = request.get_json().get('login')
        password = request.get_json().get('password')
        token = request.get_json().get('token')

        inv = self.get_invite_by(token=token)
        if not inv:
            return 'Invite not found', 200

        invite_id = inv.get('id')
        if self.get_user_by(invite_id=invite_id):
            return 'Invite was previously applied', 200

        user = self.get_user_by(
            login=login
        )
        if user:
            return 'User was previously created', 200

        user = self.add_user(
            login=login,
            password=password,
            invite_id=invite_id
        )

        user_id = user.get('id')
        session_id = token_mgr.generate_session_id()

        self.add_session(
            user_id=user_id,
            session_id=session_id
        )

        response = redirect('/')
        response.set_cookie('SESSIONID', session_id)
        response.set_cookie('UID', login)
        return response
