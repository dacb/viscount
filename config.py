import os

class Config(object):
	DEBUG = False
	TESTING = False

	BASEDIR = os.path.abspath(os.path.dirname(__file__))
	DATADIR = os.path.join(BASEDIR, 'data')

	WTF_CSRF_ENABLED = True
	# generate your own key, e.g.
	# import os
	# os.urandom(24)
	# copy it and use it here
	SECRET_KEY = 'c\xde\xb0\xc2S\x0b\x88\xbbN\x05\xf0My#\x8a\t%1\xd2\xc0.\xcf\x1c\x11'

	SQLALCHEMY_DATABASE_URI = 'mysql://viscount:viscountRocks@localhost/viscount'
	SQLALCHEMY_ECHO = False
	SQLALCHEMY_MIGRATE_REPO = os.path.join(DATADIR, 'db_repository')

	SECURITY_PASSWORD_HASH = 'bcrypt'
	SECURITY_PASSWORD_SALT = '$2a$12$BG3IinkX4A6KYpZqtMpnLO'
	SECURITY_REGISTERABLE = False
	SECURITY_CONFIRMABLE = False
	SECURITY_RECOVERABLE = False
	SECURITY_TRACKABLE = True

	INCOMING_DIR = "/home/viscount/data/incoming"
	ALLOWED_EXTENSIONS = set(['fq', 'fq.gz', 'fastq', 'fastq.gz', 'fqz', 'fa', 'fa.gz', 'fasta', 'fasta.gz', 'faz'])


class DebugConfig(Config):
	DEBUG = True
	#SQLALCHEMY_ECHO = True


class TestingConfig(Config):
	TESTING = True
	# I'm on the fence as to if this a good idea or not... shouldn't we run unit
	# tests again the production database type (e.g. mysql)
	SQLALCHEMY_DATABASE_URI = 'mysql://viscount:viscountRocks@localhost/viscount_test'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
	WTF_CSRF_ENABLED = False
