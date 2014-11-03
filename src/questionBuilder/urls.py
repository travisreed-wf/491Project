import views


def setup_urls(app):
    app.add_url_rule('/questionBuilder', view_func=views.QuestionBuilderView.as_view('questionBuilder'))
    app.add_url_rule('/quizBuilder', view_func=views.QuizBuilderView.as_view('quizBuilder'))
    app.add_url_rule('/elements/multipleChoice', view_func=views.MultipleChoiceView.as_view('elements/multipleChoice'))
    app.add_url_rule('/elements/trueFalse', view_func=views.TrueFalseView.as_view('elements/trueFalse')) 
    app.add_url_rule('/elements/freeResponse', view_func=views.FreeResponseView.as_view('elements/freeResponse'))   
    app.add_url_rule('/elements/video', view_func=views.VideoView.as_view('elements/video'))   