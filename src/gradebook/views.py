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