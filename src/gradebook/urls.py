from flask import render_template
from gradebook import views


def setup_urls(app):
    """URLs for the gradebook functions"""

    app.add_url_rule('/gradebook', view_func=views.GradebookScreenView.as_view('gradebook'))