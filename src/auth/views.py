import auth

import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
import flask_login
from flask_login import current_user
from flask_login import login_required
import models
import re
import json

class LoginView(MethodView):

    def get(self):
        if current_user is not None and current_user.is_authenticated():
            return redirect(url_for('home'))
        return render_template("login.html", failure=False)

    def post(self):
        email = flask.request.form.get('email')
        pw = flask.request.form.get('password')
        auth.login(email, pw)
        if current_user.is_authenticated():
            next_url = flask.request.args.get('next', url_for("home"))
            return redirect(next_url, code=302)
        return render_template("login.html", failure=True)


class LogoutView(MethodView):

    def get(self):
        flask_login.logout_user()
        return redirect(url_for("login"))

class RegisterView(MethodView):

    def get(self):
        return render_template('register.html')

    def post(self):
        data = flask.request.get_json()
        email = data.get('email')
        emailConfirm = data.get('emailConfirm')
        password = data.get('password')
        passwordConfirm = data.get('passwordConfirm')
        """print "Email is: " + email + "  Password is: " + password"""
        user = models.User(email, password)
        
        temp = flask.request.form.get('email')
        print temp

        models.db.session.add(user)
        models.db.session.commit()

        auth.login(email, password)
        if current_user.is_authenticated():
            print "got ehre"
            next_url = flask.request.args.get('next', url_for("home"))
            return json.dumps({"next_url": next_url})
        return render_template("register.html", failure=True)










