import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'viscount.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECURITY_CONFIRMABLE = True
SECURITY_TRACKABLE = True

FILE_DIR = 'data'
