from flask import Flask

from web.handler.auth import AuthHandler
from web.handler.invitation import InvitationHandler
from web.handler.static import StaticHandler


def create_web_app() -> Flask:
    """
    Создаем веб-сервер
    :return:
    """
    app = Flask(__name__)

    app.add_url_rule('/', methods=['GET'], view_func=StaticHandler.index)
    app.add_url_rule('/<path:path>', methods=['GET'], view_func=StaticHandler.get_resource)
    app.add_url_rule('/signin', methods=['POST'], view_func=AuthHandler().sign_in)
    app.add_url_rule('/signout', methods=['POST'], view_func=AuthHandler().sign_out)
    app.add_url_rule('/signup', methods=['POST'], view_func=AuthHandler().sign_up)
    app.add_url_rule('/send_invite', methods=['POST'], view_func=InvitationHandler().send)
    app.add_url_rule('/apply_invite/<string:token>', methods=['GET'], view_func=InvitationHandler().apply)

    return app
