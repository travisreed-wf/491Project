ISU Web Portal
===
### Primary Contributors
* Andrew Guibert
* Andrew Hartman
* Jonathan Mielke
* Lucas Rorhet
* Travis Reed 

===
### Resources
* [Trello Board](https://trello.com/b/kPAKvBao/senior-design)
* [Group Website](http://may1518.ece.iastate.edu/)
* [Project Plan](https://drive.google.com/a/iastate.edu/file/d/0B6mbCLySBSQxOUxYQ196eUY5cXc/view?usp=sharing)

### Dev Resources
* [Python Unit Testing](https://docs.python.org/2/library/unittest.html)
* [Python Mocking In Tests](https://docs.python.org/3/library/unittest.mock.html)
* [Flask](http://flask.pocoo.org/)
* [Jinja2](http://jinja.pocoo.org/docs/dev/)
* [Flask-SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/)
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [Bootstrap](http://getbootstrap.com/getting-started/)
* [Jquery](http://api.jquery.com/)

===
### Deplyoment Instructions
01. Package the source folder locally (except for the settingslocal)<br>
`zip -r build-MM-DD.zip ./src -x '*/settingslocal.py'`
02. Transfer archive to vrac server <br>
`scp ./build-MM-DD.zip username@nirwebportal.vrac.iastate.edu:/home/nirwebportal/archives/`
03. SSH into nirwebportal.vrac.iastate.edu <br>
`ssh <yourusername>@nirwebportal.vrac.iastate.edu`
04. Stop currently running server process(es) <br>
`ps -au<yourusername>` then `kill <pid>`\
05. Store the current settingslocal.py in a safe place.  Then remove old source and extract new build archive <br>
`unzip build-MM-DD.zip`
06. Replace the src folder with the new build
07. Move settingslocal.py from your safe place to the /src folder.
08. Reset database if schema changes were made since last build
09. Ensure database.db is writeable
10. Start the server <br>
`python src/run_sandbox.py 2> stderr.log &`

===
### Important Files
* models.py: Defines structure of database
* settingslocal.py: Local settings such as passwords
* run_sandbox.py: Starts the application, imports urls and initializes db
* requirements.txt: Lists out dependencies. Can be installed using pip install -Ur requirements.txt
* static/bootstrap3/css/custom-styling.css: Custom CSS

===
### General Structure
Each module has a views.py and a file or folder in templates. Work is done in the view function, then data is passed from the view function to the html, and rendered with jinja.

Decorators exist in auth.auth to restrict access to pages to admins, authors, or students. Additionally, models.py defines functions to get a list of courses a given user can access.

Code that we did not write is stored in the static folder, as are uploads from users.
