"""
factories for test data

creates data for the testing modules
"""

from datetime import datetime

from factory import Factory, Sequence, LazyAttribute
from flask_security.utils import encrypt_password

from viscount.core import db
from viscount.models import *
from viscount.users.models import Role


class CommitOnCreateFactory(Factory):
	@classmethod
	def _create(cls, target_class, *args, **kwargs):
		obj = target_class(*args, **kwargs)
		db.session.add(obj)
		db.session.commit()
		return obj
		return createModelFunction


class RoleFactory(CommitOnCreateFactory):
	FACTORY_FOR = Role
	name = 'admin'
	description = 'Administrator'


class UserFactory(CommitOnCreateFactory):
	FACTORY_FOR = User
	email = Sequence(lambda n: 'user{0}@example.com'.format(n))
	username = Sequence(lambda n: 'user{0}'.format(n))
	password = LazyAttribute(lambda a: encrypt_password('password'))
	last_login_at = datetime.utcnow()
	current_login_at = datetime.utcnow()
	last_login_ip = '127.0.0.1'
	current_login_ip = '127.0.0.1'
	login_count = 1
	roles = LazyAttribute(lambda _: [RoleFactory()])
	active = True


class ProjectFactory(CommitOnCreateFactory):
	FACTORY_FOR = Project
	name = Sequence(lambda n: 'project #{0}'.format(n))


class FileFactory(CommitOnCreateFactory):
	FACTORY_FOR = File
	name = Sequence(lambda n: 'file #{0}'.format(n))


class WorkflowFactory(CommitOnCreateFactory):
	FACTORY_FOR = Workflow
	name = Sequence(lambda n: 'workflow #{0}'.format(n))


class TaskFactory(CommitOnCreateFactory):
	FACTORY_FOR = Task
	name = Sequence(lambda n: 'task #{0}'.format(n))


class JobFactory(CommitOnCreateFactory):
	FACTORY_FOR = Job
	name = Sequence(lambda n: 'job #{0}'.format(n))


class WorkerFactory(CommitOnCreateFactory):
	FACTORY_FOR = Worker
	name = Sequence(lambda n: 'worker #{0}'.format(n))


