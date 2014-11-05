import os.path
from migrate.versioning import api
from flask.ext.script import Manager, prompt_bool
from flask.ext.security.utils import encrypt_password
from datetime import datetime
import bcrypt

from config import Config

from . import app
from ..core import db

manager = Manager(usage="Perform database operations")

@manager.command
def drop():
	"Drops database tables"
	if prompt_bool("Are you sure you want to lose all your data"):
		db.drop_all()

@manager.command
def create(default_data=True, sample_data=True):
	"Creates database tables from sqlalchemy models"
	db.create_all()
	if not os.path.exists(Config.SQLALCHEMY_MIGRATE_REPO):
		api.create(Config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
		api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	populate(default_data, sample_data)


@manager.command
def recreate(default_data=True, sample_data=True):
	"Recreates database tables (same as issuing 'drop' and then 'create')"
	drop()
	create(default_data, sample_data)


@manager.command
def populate(default_data=True, sample_data=True):
	"Populate database with default data"

	if default_data:
		from viscount.services import roles, users, file_types, tasks, task_input_files, task_output_files
		role_admin = roles.create(name='admin', description='administrator')
		role_user = roles.create(name='user', description='user')
		roles.create(name='guest', description='guest (read only)')
		admin = users.create(email='admin@host', username='admin', password=encrypt_password('password'), 
			firstName="", lastName="",
			roles = [ role_admin, role_user ])
		fasta_file_type = file_types.create(name='FASTA', description='FASTA formatted sequence file')
		fastq_file_type = file_types.create(name='FASTQ', description='FASTQ formatted sequence file')
		genbank_file_type = file_types.create(name='Genbank', description='Genbank formatted locus annotation file')
		gff_file_type = file_types.create(name='GFF', description='GFF formatted annotation file')
		fastq2fasta = tasks.create(name='FASTQ to FASTA', description='Convert a FASTQ to a FASTA', creator_id=admin.id)
		fa2fq_fq_input_file = task_input_files.create(task=fastq2fasta, file_type=fastq_file_type, name='FASTQ', description='FASTQ to convert to FASTA')
		fa2fq_fa_output_file = task_output_files.create(task=fastq2fasta, file_type=fasta_file_type, name='FASTA', description='FASTA output from FASTQ conversion')
		genbank2gff = tasks.create(name='Genbank to GFF', description='Convert a Genbank to a GFF', creator_id=admin.id)
		gb2gff_input_file = task_input_files.create(task=genbank2gff, file_type=genbank_file_type, name='Genbank', description='Genbank to convert to GFF')
		gb2gff_output_file = task_output_files.create(task=genbank2gff, file_type=gff_file_type, name='GFF', description='GFF output from Genbank conversion')


	if sample_data:
		from viscount.services import projects
		for i in range(1, 12):
			projects.create(name='Project #' + str(i), description='Example project #' + str(i), owner_id = admin.id)

@manager.command
def migrate():
	"Migrate data model"

	v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	migration = Config.SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
	tmp_module = imp.new_module('old_model')
	old_model = api.create_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	exec(old_model, tmp_module.__dict__)
	script = api.make_update_script_for_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
	open(migration, "wt").write(script)
	api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	print('New migration saved as ' + migration)
	print('Current database version: ' + str(v))

@manager.command
def upgrade():
	"Upgrade data model"

	api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	print('Current database version: ' + str(v))

@manager.command
def downgrade():
	"Downgrade data model"

	v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	api.downgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO, v - 1)
	v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
	print('Current database version: ' + str(v))
