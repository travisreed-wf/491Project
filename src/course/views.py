import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
import flask_login
from flask_login import current_user
from flask_login import login_required
import json

import models
from auth import auth


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
        course = models.Course.query.filter_by(name=courseID).first()
        author = models.User.query.filter_by(id=course.teacher_id).first()
        return render_template("course.html", course=course, author=author)


class RegisterForCourseView(MethodView):
    decorators = [login_required, auth.permissions_student]
    def get(self):

        return render_template("RegisterForCourse.html")

    def post(self):
        return "TEST"

class searchCourseName(MethodView):
    def get(self):
        return 

    def post(self):
        data = flask.request.get_json()
        courseName = data.get('courseName')
        if courseName:    
            courses = models.Course.query.filter(models.Course.name.contains(courseName)).all()
        else: 
            courses =[]
        course_info = [course.serialize for course in courses] 
        print courseName
        print course_info
        return json.dumps(course_info)

class searchProfessorName(MethodView):
    def get(self):
        return

    def post(self):
        return "Test"

class securityCode(MethodView):
    def get(self):
        return

    def post(self):

        data = flask.request.get_json()
        securityCode = data.get('securityCode')
        courseId = data.get('courseId')
        course = models.Course.query.filter_by(id=courseId).first()
        user_Courses = current_user.courses
        if securityCode == course.securityCode:
            if course in user_Courses:
                return "Already Registered"
            else:
                current_user.courses.append(course)
                models.db.session.commit()
                author = models.User.query.filter_by(id=course.teacher_id).first()
                return "Redirect to:%s" % (url_for("view_course", courseID=course.name))
        else:
            return "Security Code Incorrect"



