import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.join(BASEDIR, 'data')

WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATADIR, 'viscount.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(DATADIR, 'db_repository')

SECURITY_CONFIRMABLE = True
SECURITY_TRACKABLE = True

UPLOAD_DEST = 'uploads'
ALLOWED_EXTENSIONS = set(['fq', 'fq.gz', 'fastq', 'fastq.gz', 'fqz', 'fa', 'fa.gz', 'fasta', 'fasta.gz', 'faz'])
