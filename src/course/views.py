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
        name = flask.request.form.get('name')
        f = flask.request.files.get('students')
        course = models.Course(name)
        current_user.courses.append(course)
        course.teacher_id = current_user.id
        models.db.session.commit()
        course.set_students(f)
        return "Successful"


class CourseMasterView(MethodView):
    def get(self, courseID):
        course = models.Course.query.filter_by(name=courseID).first()
        author = models.User.query.filter_by(id=course.teacher_id).first()
        return render_template("course.html", course=course, author=author)