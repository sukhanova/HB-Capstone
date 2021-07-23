from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from datetime import datetime
import time
from model import User, Entry, Project, Task, Note, connect_to_db, db
import os

import cloudinary as Cloud
import cloudinary.uploader
import cloudinary.api
from cloudinary.uploader import upload

app = Flask(__name__)

app.config.from_pyfile('config.py')

cloudinary.config(
  cloud_name = app.config['CLOUDINARY_CLOUD_NAME'],  
  api_key = app.config['CLOUDINARY_API_KEY'],  
  api_secret = app.config['CLOUDINARY_API_SECRET']
  )

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# ------- Guest Routes ------- :

@app.route("/")
def homepage():
	"""Homepage to login or create new profile."""

	return render_template("welcome.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
	"""User registration/create a profile page"""

	if request.method == "POST":
		fname = request.form["fname"]
		lname = request.form["lname"]
		email = request.form["email"]
		password = request.form["password"]
		passwordConfirmation = request.form['passwordConfirmation']
		
		if password == passwordConfirmation:
			new_user = User(fname=fname, lname=lname, email=email)
			new_user.create_password(password)
		else:
			del new_user['passwordConfirmation']

		db.session.add(new_user)
		db.session.commit()

		user_id = new_user.user_id
		session["user_id"] = user_id

		return redirect(f"/users_dashboard/{user_id}")
	else:
		return redirect("/")


# ------- Auth Routes -------:

@app.route("/api/auth", methods=["POST"])
def login_process():
	"""Have a user login."""
		
	user = User.query.filter_by(email=request.form.get('email')).first()
	user_id = user.user_id
	
	if user.is_valid_password(request.form.get('password')):
		session['user_id'] = user.user_id
		return redirect(f"/users_dashboard/{user_id}")
	else:
		return redirect("/")


@app.route("/logout")
def logout():
	"""User logout."""

	del session["user_id"]
	return redirect(f"/")


# ------- User Routes -------:

@app.route("/users_dashboard/<int:user_id>")
def users_dashboard(user_id):
	"""This is the user's dashboard."""
	 
	projects = Project.query.filter_by(user_id=user_id).all()
	tasks = Task.query.filter_by(user_id=user_id).all()
	entries = Entry.query.filter_by(user_id=user_id).all()
	notes= Note.query.filter_by(user_id=user_id).all()

	return render_template("users_dashboard.html",
						   projects=projects,
						   user_id=user_id,
						   tasks=tasks,
						   entries=entries,
						   notes=notes)


@app.route("/create_project", methods=["GET","POST"])
def create_project():
	"""Create a new project."""

	if request.method == "POST":

		user_id = session["user_id"]
		project_name = request.form["project_name"]
		description = request.form["description"]
		project = Project(project_name=project_name,
					description=description,
					user_id=user_id)

		db.session.add(project)
		db.session.commit()

		project_id = project.project_id

		return redirect(f"/users_dashboard/{user_id}") 

	else:
		return render_template("create_project.html")

	if request.method == "GET": 
								
		user_id = session["user_id"]
		return redirect(f"/create_project/{project_id}")


@app.route("/project/<int:project_id>")
def get_project(project_id):
	"""Search for a project."""
	
	
	project = Project.query.get(project_id)
	name = project.project_name
	description = project.description
	entries = project.entries
	user_id = project.user_id
	# projects = []
	

	if user_id: 
		# for project in projects:
		# 	project_id = Project.query.get(project_id)
		# 	name = project.project_name
		# 	projects.append(name)

		return render_template("project.html",
							project=project,
							name=name,
							description=description,
							user_id=user_id)


@app.route("/select_project")
def select_project():
	user_id = session["user_id"]
	projects = Project.query.filter_by(user_id=user_id).order_by(Project.project_name.asc()).all()

	next_project = request.args.get("next_project")

	return render_template("projects_selector.html",
							projects=projects,
							next_project=next_project)


@app.route("/add_task/<int:project_id>", methods=["GET", "POST"])
def add_task(project_id):
	"""Add task to the project."""

	project = Project.query.get(project_id)

	if request.method == "POST":
		user_id = session["user_id"]
		description = request.form["description"]
		status = request.form["status"]

		task = Task(user_id=user_id,
              description=description,
              status=status)

		task.projects = [project]

		db.session.add(task)
		db.session.commit()

		task_id = task.task_id

		return redirect(f"/tasks/{task_id}")

	else:
		return render_template("create_task.html",
								project_id=project_id)


@app.route("/tasks/<int:task_id>")
def get_task(task_id):
	"""Search for a task from a project."""

	task = Task.query.get(task_id)
	user_id = session["user_id"]
	if task.user_id != session["user_id"]:
		return redirect("/")

	return render_template("tasks.html",
							task=task)
 
 
@app.route("/update_task/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    """Update task"""
    
    task = Task.query.get(task_id)
    if request.method == "POST":
        user_id = session["user_id"]
        task.description = request.form.get("description")
        task.status = request.form.get("status")
        db.session.commit()
        # return render_template("update_task.html", task=task)
        return redirect(f"/tasks/{task_id}")
    
    else:
        return render_template("update_task.html", task=task)
  
    
@app.route("/add_entry/<int:project_id>", methods=["GET", "POST"])
def add_entry(project_id):
	"""User can add an entry to their project."""
	
	user_id = session["user_id"]
	
	if request.method == "POST":
		title = request.form["title"]
		text = request.form["entry"]
		all_numbers = datetime.now().timestamp()
		time_stamp = time.ctime(all_numbers)
		image_url = None

		entry = Entry(title=title,
					entry=text,
					user_id=user_id, 
					project_id=project_id,
					time_stamp=time_stamp,
					attachment=image_url)

		db.session.add(entry)
		db.session.commit()

		return redirect(f"/users_dashboard/{user_id}")	

	else:
		return render_template("create_entry.html",
								project_id=project_id,
								user_id=user_id)


@app.route("/attachments")
def attachments():
	 
	user_id = session["user_id"]
	projects = Project.query.filter_by(user_id=user_id).all()
	entries = Entry.query.filter_by(user_id=user_id).all()
	attachments = map(lambda entry: entry.attachment, entries)
 
	if user_id:
		return render_template("attachments.html",
								attachments=attachments)
	else:
		return redirect("/select_project")


@app.route("/entry/<int:entry_id>")
def get_entry(entry_id):
	"""Search for entries in a project."""

	entry = Entry.query.get(entry_id)
	
	if entry.user_id != session["user_id"]:
		return redirect("/")

	return render_template("entries.html",
							entry=entry)


@app.route("/add_note", methods=["GET", "POST"])
def add_note():
	"""User can add short notes."""

	user_id = session["user_id"]

	if request.method == "POST":
		note = request.form["note"]
		new_note = Note(note=note, user_id=user_id)

		db.session.add(new_note)
		db.session.commit()

		return jsonify({"note_id": new_note.note_id, "note": new_note.note})
	else:
		return redirect(f"/")


@app.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    """Delete note from dashboard"""
    if request.method == "POST":
        user_id = session["user_id"]
        note_to_delete = Note.query.get(note_id)
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect(f"/users_dashboard/{user_id}")
    else:
        return redirect(f"/")

    	
		
if __name__ == "__main__":
    connect_to_db(app)
    app.config['CLOUDINARY_CLOUD_NAME'] = True
    app.config['CLOUDINARY_API_KEY'] = True
    app.config['CLOUDINARY_API_SECRET'] = True
    
    app.run(host='0.0.0.0', debug=True)