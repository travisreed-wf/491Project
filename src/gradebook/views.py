import flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import login_required
from flask_login import current_user

import models


class GradebookScreenView(MethodView):
    decorators = [login_required]

    def get(self):
        if current_user.permissions == 1:
            data = []
            for c in current_user.courses:
                tasks = []
                d = {
                    'course': c,
                }
                for task in c.tasks:
                    response = models.TaskResponse.query.filter(
                        models.TaskResponse.student_id==current_user.id,
                        models.TaskResponse.task_id==task.id).order_by(
                        models.TaskResponse.datetime.desc()).first()
                    t = {
                        'task': task,
                        'response': response
                    }
                    tasks.append(t)
                d['tasks'] = tasks
                data.append(d)
            return render_template('studentGradebook.html',
                                   courses=current_user.courses,
                                   tasks=data)
        elif current_user.permissions == 2:
            return render_template('authorGradebook.html')


class CourseGradeView(MethodView):

    def get(self, courseID):
        course = models.Course.query.filter_by(id=int(courseID) - 1000).first()
        data = []
        for u in course.users:
            if u.id != current_user.id:
                tasks = []
                d = {'user' : u}
                for task in course.tasks:
                    response = models.TaskResponse.query.filter(models.TaskResponse.task_id == task.id, models.TaskResponse.student_id == u.id).order_by(
                        models.TaskResponse.datetime.desc()).first()
                    r = {
                        'task': task,
                        'response': response
                    }
                    tasks.append(r)
                d['tasks'] = tasks
                data.append(d)
        course_tasks = {
            'course_tasks' : course.tasks
        }
        if course in current_user.courses:
            return render_template("courseGrades.html", data = data, course_tasks = course_tasks)
        else:
            return render_template("home.html")
