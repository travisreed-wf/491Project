import views


def setup_urls(app):
    app.add_url_rule('/taskBuilder', view_func=views.TaskBuilderView.as_view('taskBuilder'))
    app.add_url_rule('/task/<taskID>', view_func=views.TaskView.as_view('task_view'))
    app.add_url_rule('/elements/multipleChoice', view_func=views.MultipleChoiceView.as_view('elements/multipleChoice'))
    app.add_url_rule('/elements/trueFalse', view_func=views.TrueFalseView.as_view('elements/trueFalse')) 
    app.add_url_rule('/elements/freeResponse', view_func=views.FreeResponseView.as_view('elements/freeResponse'))   
    app.add_url_rule('/elements/video', view_func=views.VideoView.as_view('elements/video'))   