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
import json


class CreateView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("courseCreation.html")

    def post(self):
        return 200