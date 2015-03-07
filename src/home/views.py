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
        if current_user.is_authenticated():
            return flask.json.dumps([c.serialize for c in current_user.courses])
        else:
            return flask.json.dumps([])


class TaskListView(MethodView):
    def get(self):
        tasks = {'current':[], 'complete':[]}
        try:
            userResponseIDs = [tr.task_id for tr in current_user.task_responses]
        except:
            userResponseIDs = []
        for c in current_user.courses:
            for t in c.tasks:
                if(t.id in userResponseIDs):
                    tasks['complete'].append(t.serialize)
                else:
                    tasks['current'].append(t.serialize)
        tasks['complete'] = sorted(tasks['complete'], key=lambda k: k['duedate'])
        tasks['current'] = sorted(tasks['current'], key=lambda k: k['duedate'])
        return flask.json.dumps(tasks)

        