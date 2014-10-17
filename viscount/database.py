from flask.ext.sqlalchemy import SQLAlchemy

from viscount import app

db = SQLAlchemy(app)

def init_user(username, password, role):
	from viscount.user import User
	from viscount.event import Event
	user = User(username=username, password=password, role=role)
	db.session.add(user)
	db.session.add(Event(type='created', user=user))
	return user

def init_project(name, description, user):
	from viscount.project import Project
	from viscount.event import Event
	project = Project(name=name, description=description)
	db.session.add(project)
	db.session.add(Event(type='created', project=project, user=user))
	return project

def init_defaults():
	from viscount.event import Event
	db.session.add(Event(type='created'))
	init_user(username='admin', password='admin', role='admin')
	init_user(username='user', password='user', role='user')
	init_user(username='guest', password='guest', role='guest')
	db.session.commit()

def init_samples():
	from viscount.user import User
	admin = db.session.query(User).get(1)
	for i in range(16):
		init_project(name='sample' + str(i), description='sample project ' + str(i), user=admin)
	db.session.commit()
