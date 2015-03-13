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
        grader.grade_supplementary_material(responseID)
        task_response = models.TaskResponse.query.filter_by(id=responseID).first()
        formatted_time = task_response.datetime.strftime("%a %b %d %H:%M:%S")
        response = json.loads(task_response.graded_response)
        supplementary = json.loads(task_response.graded_supplementary)

        return render_template("grading/response.html", response=response,
                               student=task_response.user, task=task_response.task,
                               task_response=task_response, time=formatted_time,
                               supplementary=supplementary,
                               permissions=current_user.permissions)


class ManualGradingView(MethodView):
    decorators = [login_required]
    # TODO come back and verify that the user has permission to do this

    def post(self):
        data = flask.request.get_json()
        response = models.TaskResponse.query.filter_by(id=data['response_id']).first()
        graded_response = json.loads(response.graded_response)
        for question in graded_response['manual_questions']:
            if question['questionID'] == data['question_id']:
                question['correct'] = data['correct']
        response.graded_response = json.dumps(graded_response)
        models.db.session.commit()
        return "success"