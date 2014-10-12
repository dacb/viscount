#!venv/bin/python
import os.path
import datetime

from migrate.versioning import api

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

from viscount.server import db
from viscount.auth import User
from viscount.project import Project
from viscount.logging import Log
from viscount.file import File

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

# add default user
admin = User(username='admin', password='admin', active=True, role='admin')
db.session.add(admin)
user = User(username='user', password='user', active=True, role='user')
db.session.add(user)
user = User(username='guest', password='guest', active=True, role='guest')
db.session.add(user)

# create a log message
admin = db.session.query(User).filter_by(username = 'admin').first()
log_entry = Log(user_id = admin.id, type = 'created', message='Database (re)initialized')
db.session.add(log_entry)

# create an example project
project = Project(name='example', description='example project')
db.session.add(project)

# save the data
db.session.commit()
