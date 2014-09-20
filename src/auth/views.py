import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import login_required


class LoginView(MethodView):

    def get(self):
        return render_template("login.html", failure=False)

    def post(self):
        username = flask.request.form.get('email')
        pw = flask.request.form.get('password')
        user.login(username, pw)
        if current_user.is_authenticated():
            next_url = flask.request.args.get('next', url_for('home'))
            return redirect(next_url, code=302)
        return render_template("login.html", failure=True)
