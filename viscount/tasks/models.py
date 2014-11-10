"""
viscount.task.models

Task models
"""

from ..core import db
from ..utils import JSONSerializer


class TaskInputFile(JSONSerializer, db.Model):
	__tablename__ = 'tasks_input_files'

	id = db.Column(db.Integer, primary_key=True)
	task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
	file_type_id = db.Column(db.Integer, db.ForeignKey('file_types.id'), nullable=False)
	name = db.Column(db.String(255), nullable=False, primary_key=True)
	description = db.Column(db.Text, nullable=False)


class TaskOutputFile(JSONSerializer, db.Model):
	__tablename__ = 'tasks_output_files'

	id = db.Column(db.Integer, primary_key=True)
	task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
	file_type_id = db.Column(db.Integer, db.ForeignKey('file_types.id'), nullable=False)
	name = db.Column(db.String(255), nullable=False, primary_key=True)
	description = db.Column(db.Text, nullable=False)


class TaskJSONSerializer(JSONSerializer):
	__json_modifiers__ = {
		'events': lambda events, _: [dict(id=event.id) for event in events],
		'inputs': lambda inputs, _: [dict(id=input.id) for input in inputs],
		'outputs': lambda outputs, _: [dict(id=output.id) for output in outputs],

		'task_instances': lambda task_instances, _: [dict(id=task_instance.id) for task_instance in task_instances],
	}


class Task(TaskJSONSerializer, db.Model):
	__tablename__ = 'tasks'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	description = db.Column(db.Text, index=False, unique=False, nullable=False)
	source_file = db.Column(db.Integer, db.ForeignKey('files.id'))

	events = db.relationship('Event', backref='task', lazy='dynamic')
	inputs = db.relationship('TaskInputFile', backref='task', lazy='dynamic')
	outputs = db.relationship('TaskOutputFile', backref='task', lazy='dynamic')

	task_instances = db.relationship('WorkflowTaskInstance', backref='task', lazy='dynamic')

	def __repr__(self):
		return '<Task %r>' % (self.name)
