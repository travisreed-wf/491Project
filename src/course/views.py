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
        title = flask.request.form.get('title')
        course = models.Course(name,title)
        current_user.courses.append(course)
        course.teacher_id = current_user.id
        models.db.session.commit()
        author = models.User.query.filter_by(id=course.teacher_id).first()
        if f:
            course.set_students(f)
        return render_template("course.html", course=course, author=author)


class CourseMasterView(MethodView):
    def get(self, courseID):
        course = models.Course.query.filter_by(id=int(courseID) - 1000).first()
        author = models.User.query.filter_by(id=course.teacher_id).first()
        if course in current_user.courses:
            return render_template("course.html", course=course, author=author)
        else:
            return render_template("home.html");