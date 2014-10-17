import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.join(BASEDIR, 'data')

WTF_CSRF_ENABLED = True
# generate your own key, e.g.
# import os
# os.urandom(24)
# copy it and use it here
SECRET_KEY = 'c\xde\xb0\xc2S\x0b\x88\xbbN\x05\xf0My#\x8a\t%1\xd2\xc0.\xcf\x1c\x11'

SQLALCHEMY_DATABASE_URI = 'mysql://viscount:viscountRocks@localhost/viscount'
#SQLALCHEMY_ECHO = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(DATADIR, 'db_repository')

SECURITY_CONFIRMABLE = True
SECURITY_TRACKABLE = True

UPLOAD_DEST = os.path.join(DATADIR, 'uploads')
ALLOWED_EXTENSIONS = set(['fq', 'fq.gz', 'fastq', 'fastq.gz', 'fqz', 'fa', 'fa.gz', 'fasta', 'fasta.gz', 'faz'])
