from flask_login import LoginManager
import models


def initialize(app):
    loginmanager = LoginManager()
    loginmanager.init_app(app)
    loginmanager.user_loader(load_user)
    loginmanager.login_view = "login"
    loginmanager.login_message = None


def load_user(username):
    return models.User.get_by_username(username)