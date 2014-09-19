from flask import render_template
from home import views


def setup_urls(app):
    """URLs for the Home functions"""

    app.add_url_rule('/home', view_func=views.HomeScreenView.as_view('home'))
