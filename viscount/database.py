from flask.ext.sqlalchemy import SQLAlchemy

from viscount import app

db = SQLAlchemy(app)

def init_defaults():
	from viscount.user import userCreate
	userCreate('admin', 'admin', 'admin')
	userCreate('user', 'user', 'user')
	userCreate('guest', 'guest', 'guest')

def init_samples():
	from viscount.user import projectCreate
	admin = db.session.query(User).get(1)
	for i in range(16):
		projectCreate('sample' + str(i), 'sample project ' + str(i), admin)
