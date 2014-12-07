import re

import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import login_required

import auth
from auth import auth
import helper_functions
import models


class TaskBuilderView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        elements = helper_functions.get_elements()
        print "GOT TO TAKSBUILDER"
        return render_template("taskBuilder.html", elements=elements)

    def post(self):
        task = models.Task()
        pattern = r"<script.*?</script>"
        content = flask.request.data
        task.content = re.sub(pattern, "", content, flags=re.DOTALL)
        models.db.session.add(task)
        models.db.session.commit()
        return ""


class TaskView(MethodView):
    decorators = [login_required]

    def get(self, taskID):
        task = models.Task.query.filter_by(id=taskID).first()
        print task.content
        content = "<div></div>"
        return render_template("taskView.html", content=task.content.strip().replace('\n', ''))


class MultipleChoiceView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        return render_template("elements/multipleChoice.html")


class TrueFalseView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        return render_template("elements/trueFalse.html")


class FreeResponseView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        return render_template("elements/freeResponse.html")


class SupplementaryView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        return render_template("elements/supplementary.html")
