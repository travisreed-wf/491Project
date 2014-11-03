import views


def setup_urls(app):
    app.add_url_rule('/course/create', view_func=views.CreateView.as_view('create_course'))
