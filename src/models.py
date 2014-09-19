from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    displayname = db.Column(db.Unicode(255))

    def __init__(self, username, email, displayname):
        self.username = username
        self.email = email
        self.displayname = displayname
        return