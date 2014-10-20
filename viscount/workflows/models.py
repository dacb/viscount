"""
viscount.workflow.models

Workflow models
"""

from ..core import db
from ..utils import JSONSerializer


workflows_tasks = db.Table(
		'workflows_tasks',
		db.Column('workflow_id', db.Integer(), db.ForeignKey('workflows.id')),
		db.Column('task_id', db.Integer(), db.ForeignKey('tasks.id'))
	)


class WorkflowJSONSerializer(JSONSerializer):
	__json_modifiers__ = {
		'tasks': lambda tasks, _: [dict(id=task.id) for task in tasks],
		'events': lambda events, _: [dict(id=event.id) for event in events],
		'revisions': lambda revisions, _: [dict(id=workflow.id) for revision in revisions]
	}


class Workflow(WorkflowJSONSerializer, db.Model):
	__tablename__ = 'workflows'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.Text, index=False, unique=False)
	revision = db.Column(db.Integer, nullable=False, default=0)
	revised_from_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))

	events = db.relationship('Event', backref='workflow', lazy='dynamic')
	tasks = db.relationship('Task', secondary=workflows_tasks, backref=db.backref('workflows', lazy='joined'))
	revisions = db.relationship('Workflow', backref=db.backref('revised_from', remote_side=id), lazy='dynamic')
				

	def __repr__(self):
		return '<Workflow %r>' % (self.name)
