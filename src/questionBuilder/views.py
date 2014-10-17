import auth

import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView

class QuestionBuilderView(MethodView):

    def get(self):
        return render_template("questionBuilder.html", failure=False)
