"""
viscount.workflow.models

Workflow models
"""

from ..core import db
from ..utils import JSONSerializer


class WorkflowTaskInstance(JSONSerializer, db.Model):
	__tablename__ = 'workflows_tasks_instances'

	id = db.Column(db.Integer, primary_key=True)
	workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
	description = db.Column(db.Text, index=False, unique=False)


class WorkflowJSONSerializer(JSONSerializer):
	__json_modifiers__ = {
		'tasks': lambda tasks, _: [dict(id=task.id) for task in tasks],
		'events': lambda events, _: [dict(id=event.id) for event in events],
		'revisions': lambda revisions, _: [dict(id=workflow.id) for revision in revisions]
		# add others here
	}


class Workflow(WorkflowJSONSerializer, db.Model):
	__tablename__ = 'workflows'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.Text, index=False, unique=False)
	revision = db.Column(db.Integer, nullable=False, default=0)
	revised_from_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))

	task_instances = db.relationship('WorkflowTaskInstance', backref='workflow', lazy='dynamic')

	events = db.relationship('Event', backref='workflow', lazy='dynamic')
	revisions = db.relationship('Workflow', backref=db.backref('revised_from', remote_side=id), lazy='dynamic')


	def __repr__(self):
		return '<Workflow %r>' % (self.name)
