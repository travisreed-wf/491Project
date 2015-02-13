import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
import flask_login
from flask_login import current_user
from flask_login import login_required
import json

import grading
import models


class ResponseView(MethodView):
    decorators = [login_required]

    def get(self, responseID):
        grader = grading.Grader()
        grader.grade_automatic_questions(responseID)
        task_response = models.TaskResponse.query.filter_by(id=responseID).first()
        response = json.loads(task_response.graded_response)
        return render_template("grading/response.html", response=response,
                               student=task_response.user, task=task_response.task,
                               task_response=task_response)
        