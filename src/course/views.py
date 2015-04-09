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
        course = models.Course(name, title)
        course.teacher_id = current_user.id
        models.db.session.add(course)
        models.db.session.commit()
        author = models.User.query.filter_by(id=course.teacher_id).first()
        if f:
            course.set_students(f)
        return render_template("course.html", course=course, author=author)


class CourseMasterView(MethodView):
    decorators = [login_required]

    def get(self, courseID):
        course = models.Course.query.filter_by(id=int(courseID) - 1000).first()
        author = models.User.query.filter_by(id=course.teacher_id).first()     
        if course in current_user.courses or course.teacher_id == current_user.id or ","+str(current_user.id)+"," in course.secondaryTeachers:
            return render_template("course.html", course=course, author=author)
        else:
            return "You do not have access to view this course", 401


class CourseTaskListView(MethodView):
    def get(self, courseID):
        tasks = {'current':[], 'complete':[]}
        course = models.Course.query.filter_by(id=int(courseID) - 1000).first()
        userResponseIDs = [tr.task_id for tr in current_user.task_responses]
        for t in course.tasks:
            if t.status == "created":
                continue
            if(t.id in userResponseIDs):
                tasks['complete'].append(t.serialize)
            else:
                tasks['current'].append(t.serialize)
        tasks['complete'] = sorted(tasks['complete'], key=lambda k: k['duedate'])
        tasks['current'] = sorted(tasks['current'], key=lambda k: k['duedate'])
        return flask.json.dumps(tasks)


class RegisterForCourseView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("registerForCourse.html")

    def post(self):
        return "TEST"


class searchCourseName(MethodView):
    def get(self):
        return

    def post(self):
        data = flask.request.get_json()
        courseName = data.get('courseName')
        if courseName:
            courses = models.Course.query.filter(
                models.Course.name.contains(courseName),
                models.Course.isArchived == False).all()
        else:
            courses = []
        course_info = [course.serialize for course in courses]
        return json.dumps(course_info)

class ArchiveCourse(MethodView):
    decorators = [login_required, auth.permissions_author]

    def post(self, courseID):
        course = models.Course.query.filter_by(id=int(courseID)).first()
        course.isArchived = True
        models.db.session.add(course)
        models.db.session.commit()
        return ""

class UnarchiveCourse(MethodView):
    decorators = [login_required, auth.permissions_author]

    def post(self, courseID):
        course = models.Course.query.filter_by(id=int(courseID)).first()
        course.isArchived = False
        models.db.session.add(course)
        models.db.session.commit()
        return ""

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
                return "Redirect to:%s" % (url_for("view_course", courseID=course.id+1000))
        else:
            return "Registration Code Incorrect"

class AddTAView(MethodView):

    def get(self):
        return

    def post(self):
        data = flask.request.get_json()
        email = data.get('email')
        courseId = data.get('courseID')
        course = models.Course.query.filter_by(id=courseId).first()
        if email:
            user = models.User.query.filter(models.User.email.contains(email)).first()
            if user and user.permissions:
                    if user.permissions < 20:
                        user.permissions = 20
                    secondaryTeachers = course.secondaryTeachers
                    userIdAndComma = str(user.id) + ","
                    if secondaryTeachers.find("," + userIdAndComma) >= 0:
                        return "failure"
                    secondaryTeachers = secondaryTeachers + userIdAndComma
                    course.secondaryTeachers = secondaryTeachers
                    models.db.session.commit()
                    return email
            else: 
                return "failure"
        else:
            return "failure"

class RemoveTAView(MethodView):

    def get(self):
        return

    def post(self):
        data = flask.request.get_json()
        email = data.get('email')
        courseId = data.get('courseID')
        course = models.Course.query.filter_by(id=courseId).first()
        if email:
            user = models.User.query.filter(models.User.email.contains(email)).first()
            if user and user.permissions:
                newUser = models.User.query.filter_by(email=email).first()
                tas = models.Course.query.filter(models.Course.secondaryTeachers.contains(","+str(newUser.id)+",")).all()
                if len(tas) <= 1 and user.permissions == 20:
                    newUser.permissions = 10
                secondaryTeachers = course.secondaryTeachers
                userIdAndComma = "," + str(user.id) + ","
                print secondaryTeachers.find(userIdAndComma)
                if secondaryTeachers.find(userIdAndComma) >=0:
                    secondaryTeachers = secondaryTeachers.replace(userIdAndComma,",",1)
                else:
                    return "failure"
                course.secondaryTeachers = secondaryTeachers
                models.db.session.commit()
                return email
            else: 
                print "((((((((((("
                return "failure"
        else:
            return "failure"