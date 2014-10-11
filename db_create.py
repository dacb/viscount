#!venv/bin/python
import os.path

from migrate.versioning import api

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

from viscount.server import db
from viscount.auth import User
from viscount.project import Project

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

# add default user
user = User(username='admin', password='admin', active=True, role='admin')
db.session.add(user)
user = User(username='user', password='user', active=True, role='user')
db.session.add(user)
user = User(username='guest', password='guest', active=True, role='guest')
db.session.add(user)
# create an example project
project = Project(name='example', description='example project')
db.session.add(project)

# save the data
db.session.commit()
