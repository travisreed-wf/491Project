import flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import login_required


class HomeScreenView(MethodView):
    #decorators = [login_required]

    def get(self):
        text = flask.request.args.get('text', "")
        return render_template('home.html', text=text)