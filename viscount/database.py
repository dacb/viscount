from flask.ext.sqlalchemy import SQLAlchemy

from viscount import app

db = SQLAlchemy(app)

def init_defaults():
	from viscount.user import User
	db.session.add(User(username='admin', password='admin', role='admin'))
	db.session.add(User(username='user', password='user', role='user'))
	db.session.add(User(username='guest', password='guest', role='guest'))
	db.session.commit()

def init_samples():
	from viscount.user import Project
	admin = db.session.query(User).get(1)
	for i in range(16):
		db.session.add(Project('sample' + str(i), 'sample project ' + str(i)))
	db.session.commit()
