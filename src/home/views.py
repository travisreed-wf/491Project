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
        # print "adsfkhladkjghsldkfjhglsjkdfhglsdjfkhg"
        # tasks=[c.tasks for c in current_user.courses]
        # return flask.json.dumps([t.serialize for t in tasks])
        hit = "hi"
        return flask.json.dumps(hit)
            
class DBButtonView(MethodView):
    def get(self):
        #user = models.User("test@test.com", "pass")
        #user = models.db.session.query(models.User).filter_by(id=1).first()
        #user.courses.append(models.db.session.query(models.Course).filter_by(id=1).first())
        #models.db.session.commit()
        print "in python"
        course = models.db.session.query(models.Course).filter_by(id=2).first()
        course.tasks.append(models.Task("Assignment 1"))
        models.db.session.commit()
        #print models.db.session.query(models.Course).filter_by(id=1).first()
        return render_template('home.html')
