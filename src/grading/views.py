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


class ResponseView(MethodView):
    decorators = [login_required]

    def get(self, responseID):
        response = models.TaskResponse.query.filter_by(id=responseID).first()
        print response.user
        return render_template("grading/response.html", response=response,
                               student=response.user, task=response.task)
        