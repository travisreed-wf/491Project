import json
import unittest

from mock import Mock
from mock import patch

import views


class TestLoginView(unittest.TestCase):

    def setUp(self):
        flask_login = patch.object(views, "flask_login")
        self.addCleanup(flask_login.stop)
        self.flask_login = flask_login.start()

        redirect = patch.object(views, "redirect")
        self.addCleanup(redirect.stop)
        self.redirect = redirect.start()

        url_for = patch.object(views, "url_for")
        self.addCleanup(url_for.stop)
        self.url_for = url_for.start()
        self.url_for.return_value = "home"

        render_template = patch.object(views, "render_template")
        self.addCleanup(render_template.stop)
        self.render_template = render_template.start()

    def test_get(self):
        current_user = Mock()
        current_user.is_authenticated.return_value = True
        self.flask_login.current_user = current_user

        views.LoginView().get()
        self.url_for.assert_called_with("home")
        self.redirect.assert_called_with("home")

    def test_get_not_authenticated(self):
        current_user = Mock()
        current_user.is_authenticated.return_value = False
        self.flask_login.current_user = current_user

        views.LoginView().get()
        self.render_template.assert_called_with("login.html", failure=False)
