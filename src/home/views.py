import flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import login_required
import flask_login
from flask_login import current_user
import models
import re
import json


class HomeScreenView(MethodView):
    decorators = [login_required]

    def get(self):
        print current_user.courses
        return render_template('home.html')


class ClassListView(MethodView):
    def get(self):
        return flask.json.dumps([c.serialize for c in current_user.courses])


class TaskListView(MethodView):
    def get(self):
        task = "task1"
        return flask.json.dumps(task)
            