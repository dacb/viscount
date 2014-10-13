#!venv/bin/python
import os.path
import datetime

from migrate.versioning import api

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

from viscount.server import db
from viscount.user import userCreate
from viscount.project import projectCreate
from viscount.log import logEntry
from viscount.job import jobCreate

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

# add default user
admin = userCreate(username='admin', password='admin', role='admin')
userCreate(username='user', password='user', role='user')
userCreate(username='guest', password='guest', role='guest')

# create an example project
project = projectCreate(name='example', description='example project', user=admin)

# create a sample job
jobCreate(admin, project, "command text")
