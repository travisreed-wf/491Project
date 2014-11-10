import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView

import auth
import helper_functions


class TaskBuilderView(MethodView):

    def get(self):
        elements = helper_functions.get_elements()
        return render_template("taskBuilder.html", elements=elements)


class MultipleChoiceView(MethodView):

    def get(self):
        return render_template("elements/multipleChoice.html")


class TrueFalseView(MethodView):

    def get(self):
        return render_template("elements/trueFalse.html")


class FreeResponseView(MethodView):

    def get(self):
        return render_template("elements/freeResponse.html")


class VideoView(MethodView):

    def get(self):
        return render_template("elements/video.html")