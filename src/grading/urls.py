from flask import render_template
import views


def setup_urls(app):
    """URLs for the Grading functions"""
    app.add_url_rule('/response/<responseID>', view_func=views.ResponseView.as_view('response'))
    app.add_url_rule('/grading/manual', view_func=views.ManualGradingView.as_view('grade_manually'))
