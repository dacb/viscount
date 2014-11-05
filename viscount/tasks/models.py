"""
viscount.task.models

Task models
"""

from ..core import db
from ..utils import JSONSerializer


tasks_input_files = db.Table(
	'tasks_input_files',
	db.Column('task_id', db.Integer(), db.ForeignKey('tasks.id')),
	db.Column('input_file_type_id', db.Integer(), db.ForeignKey('file_types.id')))


tasks_output_files = db.Table(
	'tasks_output_files',
	db.Column('task_id', db.Integer(), db.ForeignKey('tasks.id')),
	db.Column('output_file_type_id', db.Integer(), db.ForeignKey('file_types.id')))


class TaskJSONSerializer(JSONSerializer):
	__json_modifiers__ = {
		'events': lambda events, _: [dict(id=event.id) for event in events],
		'input_file_types': lambda input_file_types, _: [dict(id=file_types.id) for file_type in input_file_types],
		'output_file_types': lambda output_file_types, _: [dict(id=file_types.id) for file_type in input_file_types],
	}


class Task(TaskJSONSerializer, db.Model):
	__tablename__ = 'tasks'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.Text, index=False, unique=False)
	source_file = db.Column(db.Integer, db.ForeignKey('files.id'))

	events = db.relationship('Event', backref='task', lazy='dynamic')
	input_file_types = db.relationship('FileType', secondary=tasks_input_files, backref=db.backref('input_file_types', lazy='dynamic'))
	output_file_types = db.relationship('FileType', secondary=tasks_input_files, backref=db.backref('output_file_types', lazy='dynamic'))

	def __repr__(self):
		return '<Task %r>' % (self.name)
