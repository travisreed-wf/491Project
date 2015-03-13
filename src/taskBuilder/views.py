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

    def post(self, userid):
        f = flask.request.files.get('file_path')
        print f
        print f.filename
        print userid
        uploadDir = "src/static/uploads/" + userid
        if not os.path.exists(uploadDir):
            os.makedirs(uploadDir)
        if f and allowed_file(f.filename):
            f.save(os.path.join(uploadDir, f.filename))
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


class TaskTransitionView(MethodView):
    decorators = [login_required]

    def post(self):
        data = flask.request.get_json()
        task = models.Task.query.filter_by(id=data['task_id']).first()
        task.status = data['status']
        models.db.session.commit()
        return "success"


class TaskView(MethodView):
    decorators = [login_required]

    def get(self, taskID):
        task = models.Task.query.filter_by(id=int(taskID)).first()
        course = models.Course.query.filter_by(id=task.course_id).first()
        if current_user.id == course.teacher_id:
            return render_template("tasks/taskAuthorView.html", task=task, course=course)
        elif course.id not in [c.id for c in current_user.courses]:
            return "You are not allowed to see that task", 401
        elif task.status == "available":
            return render_template("tasks/taskStudentView.html", content=task.content.strip().replace('\n', ''))
        else:
            return "This task is no longer available"

    def post(self, taskID):
        data = flask.request.get_json()
        task_response = models.TaskResponse(json.dumps(data))
        task_response.datetime = datetime.datetime.now()
        task_response.task_id = int(taskID)
        task_response.student_id = current_user.id
        task_response.supplementary = json.dumps(data.get('supplementary'))
        start_time = data.get('startTaskTime')
        end_time = data.get('endTaskTime')
        date_format = "%m/%d/%Y %I:%M:%S %p"
        formatted_s_time = datetime.datetime.strptime(start_time, date_format)
        formatted_e_time = datetime.datetime.strptime(end_time, date_format)
        task_response.start_time = formatted_s_time
        task_response.end_time = formatted_e_time
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

class TextContentView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        return render_template("elements/textContent.html")

class CoursesTeachingView(MethodView):

    def get(self):
        return flask.json.dumps([c.serialize for c in current_user.coursesTeaching])

