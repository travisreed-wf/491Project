import flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask.views import MethodView
from flask_login import login_required

import auth
from auth import auth
import helper_functions


class TaskBuilderView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        elements = helper_functions.get_elements()
        print "GOT TO TAKSBUILDER"
        return render_template("taskBuilder.html", elements=elements)


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


class VideoView(MethodView):
    decorators = [login_required, auth.permissions_author]

    def get(self):
        return render_template("elements/video.html")