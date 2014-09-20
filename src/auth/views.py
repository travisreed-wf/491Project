import auth

import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import current_user
from flask_login import login_required


class LoginView(MethodView):

    def get(self):
        return render_template("login.html", failure=False)

    def post(self):
        email = flask.request.json.get('email')
        pw = flask.request.json.get('password')
        auth.login(email, pw)
        print flask.session.get('user_id')
        if current_user.is_authenticated():
            next_url = flask.request.args.get('next', url_for('home'))
            return redirect(next_url, code=302)
        return render_template("login.html", failure=True)
