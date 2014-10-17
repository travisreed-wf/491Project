import views


def setup_urls(app):
    app.add_url_rule('/questionBuilder', view_func=views.QuestionBuilderView.as_view('questionBuilder'))
