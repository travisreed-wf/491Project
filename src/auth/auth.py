import flask
from flask_login import LoginManager
from flask_login import login_user
import models


def initialize(app):
    loginmanager = LoginManager()
    loginmanager.init_app(app)
    loginmanager.user_loader(load_user)
    loginmanager.login_view = "login"
    loginmanager.login_message = None


def load_user(user_id):
    return models.User.query.filter_by(id=int(user_id)).first()


def login(email, password):
    user = models.User.query.filter_by(email=email).first()
    if not user:
        return False

    if user.password == password:
        flask.session['email'] = user.email
        login_user(user)
        return True
    return False
