from flask import render_template
import views

def setup_urls(app):
    """URLs for the Home functions"""

    app.add_url_rule('/home', view_func=views.HomeScreenView.as_view('home'))
    app.add_url_rule('/testDBButton', view_func=views.DBButtonView.as_view('test'))
    app.add_url_rule('/home/classlist', view_func=views.ClassListView.as_view('class_list'))
