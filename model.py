"""Models and database functions for Task Tracking dashboard"""

from flask import Flask 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, Model
from werkzeug.security import generate_password_hash, check_password_hash


SQLALCHEMY_DATABASE_URI = "postgresql:///task_tracking"
db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
	"""A user table in task_tracking database."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(25), nullable=False)
	lname = db.Column(db.String(25), nullable=False)
	email = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(), nullable=False)

	def __repr__(self):

		return f"<User user_id={self.user_id} email={self.email}>"


	def create_password(self, password):
		self.password = generate_password_hash(password)

	def is_valid_password(self, password):
		return check_password_hash(self.password, password)


class Project(db.Model):
	"""Project table in task_tracking database."""

	__tablename__ = "projects"

	project_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
	project_name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(160), nullable=True)

	entries = db.relationship("Entry", backref="trips")
	tasks = db.relationship("Task", secondary="tasks_projects", backref="projects")
	projects = db.relationship("User", backref="projects")

	def __repr__(self):

		return f"<Project project_id={self.project_id} and user_id={self.user_id}>"


class Task(db.Model):
	"""Task table in task_tracking database."""

	__tablename__ = "tasks"

	task_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
	description = db.Column(db.String(100), nullable=True)
	status = db.Column(db.String(100), nullable=True)

	def __repr__(self):

		return f"<Task task_id={self.task_id} and user_id={self.user_id}>"


class Entry(db.Model):
	"""Entry table table in task_tracking database."""

	__tablename__ = "entries"

	entry_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
	project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
	title = db.Column(db.String(100), nullable = False)
	entry = db.Column(db.String(), nullable=False)
	time_stamp = db.Column(db.String())
	attachment = db.Column(db.String(), nullable=True)
	
	user = db.relationship("User", backref="entries")
	

	def __repr__(self):

		return f"<Entry entry_id={self.entry_id}>"

class Note(db.Model):
    """Note table in task_tracking database."""
    
    __tablename__="notes"
    
    note_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    note = db.Column(db.String(), nullable=True)
    
    def __repr__(self):
        return f"<Note note_id={self.note_id}>"

    notes = db.relationship("User", backref="notes")


tasks_projects = db.Table("tasks_projects", 

	db.Column("task_id", db.Integer, db.ForeignKey("tasks.task_id"), primary_key=True),
	db.Column("project_id", db.Integer, db.ForeignKey("projects.project_id"), primary_key=True))

###################################################################
# Helper functions

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	# Configure to use our PostgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///task_tracking' 
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_ECHO'] = True
	db.app = app
	db.init_app(app)

if __name__ == "__main__":

	from server import app

	connect_to_db(app)
	#db.drop_all()
	db.create_all()

	print("Connect to DB.")