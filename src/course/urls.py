import views


def setup_urls(app):
    app.add_url_rule('/course/create', view_func=views.CreateView.as_view('create_course'))
    app.add_url_rule('/course/view/<courseID>', view_func=views.CourseMasterView.as_view('view_course'))
    app.add_url_rule('/home/coursetasklist/<courseID>', view_func=views.CourseTaskListView.as_view('course_task_list'))
    app.add_url_rule('/course/registerForCourse', view_func=views.RegisterForCourseView.as_view('register_course'))
    app.add_url_rule('/course/searchCourseName', view_func=views.searchCourseName.as_view('search_course_name'))
    app.add_url_rule('/course/searchProfessorName', view_func=views.searchProfessorName.as_view('search_course_professor'))
    app.add_url_rule('/course/securityCode', view_func=views.securityCode.as_view('security_code'))
