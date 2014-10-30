import auth

import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
import flask_login
from flask_login import current_user
from flask_login import login_required
import models
import json


class CreateView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("courseCreation.html")

    def post(self):
        user = models.User("test@test.com", "pass")
        user = models.db.session.query(models.User).filter_by(id=1).first()
        user.courses.append(models.db.session.query(models.Course).filter_by(id=1).first())
        models.db.session.commit()
        print user.courses[0].name
        print models.db.session.query(models.Course).filter_by(id=1).first()