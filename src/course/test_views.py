import json
import unittest

from mock import Mock
from mock import patch

import views


class TestSearchCourseName(unittest.TestCase):

    @patch.object(views, "models")
    @patch.object(views, "flask")
    def test_post(self, flask, models):
        data = {
            'courseName': "name"
        }
        flask.request.get_json.return_value = data
        c1 = Mock(serialize="")
        models.Course.query.filter.return_value.all.return_value = [c1]
        ret = views.SearchCourseName().post()
        self.assertEqual(ret, json.dumps([""]))


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


class TestCourseMasterView(unittest.TestCase):

    @patch.object(views, "current_user")
    @patch.object(views, "models")
    @patch.object(views, "render_template")
    def test_get(self, render_template, models, current_user):
        c = Mock()
        models.Course.query.filter_by.return_value.first.return_value = c
        current_user.get_courses_where_teacher_or_ta.return_value = [c]
        views.CourseMasterView().get(11)
        self.assertTrue(render_template.called)
