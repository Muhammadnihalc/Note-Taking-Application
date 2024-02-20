from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# this is the db for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(256), nullable=False)

# this is the db for Notess
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(100), nullable=False)
    note_text = db.Column(db.Text, nullable=False)
    note_admin = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_access = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    last_updated_time = db.Column(db.DateTime, nullable=False)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
