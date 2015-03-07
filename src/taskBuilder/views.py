import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import current_user
from flask_login import login_required
from flask_login import current_user
from werkzeug import secure_filename

import datetime
import time
import json
import os
import re

import auth
from auth import auth
import config
import helper_functions
import models


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def get_thumbnail(extension):
    if extension == "pdf":
        return models.Thumbnail.query.filter_by(id=1).first()
    elif extension == "txt":
        return models.Thumbnail.query.filter_by(id=2).first()
    elif extension == "mp3":
        return models.Thumbnail.query.filter_by(id=4).first()
    else:
        return models.Thumbnail.query.filter_by(id=3).first()


class UploadView(MethodView):

    def get(self):
        return render_template('upload.html')

    def post(self):
        f = flask.request.files.get('file_path')
        print f
        print f.filename
        if f and allowed_file(f.filename):
            f.save(os.path.join("src/static/uploads", f.filename))
            return "Success"
        return "Failed"


class UploadedFileView(MethodView):

    def get(self, filename):
        return flask.send_file("static/uploads/" + filename)


class TaskBuilderView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        elements = helper_functions.get_elements()
        return render_template("tasks/taskBuilder.html", elements=elements)

    def post(self):
        task = models.Task("")
        pattern = r"<script.*?</script>"
        data = flask.request.get_json()
        content = data.get('html')
        courseID = data.get('course_id')
        taskTitle = data.get('taskTitle')
        taskDueDate = data.get('taskDue')
        task.title = taskTitle
        task.content = re.sub(pattern, "", content, flags=re.DOTALL)
        task.questions = json.dumps(data.get('questions'))
        task.course = models.Course.query.filter_by(id=courseID).first()
        task.duedate = datetime.datetime.fromtimestamp(taskDueDate/1000.0)
        task.supplementary = json.dumps(data.get('supplementary'))
        models.db.session.add(task)
        models.db.session.commit()
        return ""


class TaskView(MethodView):
    decorators = [login_required]

    def get(self, taskID):
        task = models.Task.query.filter_by(id=int(taskID)).first()
        content = "<div></div>"
        return render_template("tasks/taskView.html", content=task.content.strip().replace('\n', ''))

    def post(self, taskID):
        print flask.request.get_json()
        task_response = models.TaskResponse(json.dumps(flask.request.get_json()))
        task_response.datetime = datetime.datetime.now()
        task_response.task_id = int(taskID)
        task_response.student_id = current_user.id
        models.db.session.add(task_response)
        models.db.session.commit()
        return "success"


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

class QuestionContentView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        return render_template("elements/questionContent.html")

class CoursesTeachingView(MethodView):

    def get(self):
        return flask.json.dumps([c.serialize for c in current_user.coursesTeaching])

