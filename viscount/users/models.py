"""
viscount.users.models

User models
"""

from flask_security import UserMixin, RoleMixin

from ..core import db
from ..utils import JSONSerializer


roles_users = db.Table(
	'roles_users',
	db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
	db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class RoleJSONSerializer(JSONSerializer):
	__json_modifiers__ = {
		'users': lambda users, _: [dict(id=user.id) for user in users]
	}


class Role(RoleJSONSerializer, RoleMixin, db.Model):
	__tablename__ = 'roles'

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.String(255))

	def __eq__(self, other):
		return (self.name == other or self.name == getattr(other, 'name', None))

	def __ne__(self, other):
		return (self.name != other and self.name != getattr(other, 'name', None))


class UserJSONSerializer(JSONSerializer):
	__json_hidden__ = ['password']
	__json_modifiers__ = {
		'roles': lambda roles, _: [dict(id=role.id) for role in roles],
		'events': lambda events, _: [dict(id=event.id) for event in events],
		'projects': lambda projects, _: [dict(id=project.id) for project in projects],
		'files': lambda files, _: [dict(id=file.id) for file in files],
		'workflows': lambda workflows, _: [dict(id=workflow.id) for workflow in workflows],
		'tasks': lambda tasks, _: [dict(id=task.id) for task in tasks],
		'jobs': lambda jobs, _: [dict(id=job.id) for job in jobs],
	}


class User(UserJSONSerializer, UserMixin, db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	username = db.Column(db.String(32), unique=True)
	password = db.Column(db.String(120))
	firstName = db.Column(db.String(32))
	lastName = db.Column(db.String(32))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	last_login_at = db.Column(db.DateTime())
	current_login_at = db.Column(db.DateTime())
	last_login_ip = db.Column(db.String(15))
	current_login_ip = db.Column(db.String(15))
	login_count = db.Column(db.Integer)
	registered_at = db.Column(db.DateTime())

	roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

	events = db.relationship('Event', backref='user', lazy='dynamic')
	projects = db.relationship('Project', backref='owner', lazy='dynamic')
	files = db.relationship('File', backref='owner', lazy='dynamic')
	workflows = db.relationship('Workflow', backref='owner', lazy='dynamic')
	tasks = db.relationship('Task', backref='owner', lazy='dynamic')
	jobs = db.relationship('Job', backref='owner', lazy='dynamic')
