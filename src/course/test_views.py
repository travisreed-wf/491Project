import json
import unittest

from mock import Mock
from mock import patch

import views


class TestCreateView(unittest.TestCase):

    @patch.object(views, "render_template")
    def test_get(self, render_template):
        views.CreateView().get()
        render_template.assert_called_with("courseCreation.html")

    @patch.object(views, "current_user")
    @patch.object(views, "render_template")
    @patch.object(views, "models")
    @patch.object(views, "flask")
    def test_post(self, flask, models, render_template, current_user):
        flask.request.form = {'name': "MATH-100", 'title': "title"}
        flask.request.files = {'students': "f"}
        course = Mock()
        models.Course.return_value = course
        views.CreateView().post()
        models.Course.assert_called_with("MATH-100", "title")
        self.assertTrue(models.db.session.commit.called)
        course.set_students.assert_called_with("f")