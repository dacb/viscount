"""
viscount.workflow.models

Workflow models
"""

from ..core import db
from ..utils import JSONSerializer


# nodes in a workflow graph
class WorkflowTaskInstance(JSONSerializer, db.Model):
	__tablename__ = 'workflows_tasks_instances'

	id = db.Column(db.Integer, primary_key=True)
	workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
	description = db.Column(db.Text, index=False, unique=False)


# edges in a workflow graph
class WorkflowTaskInstanceIO(JSONSerializer, db.Model):
	__tablename__ = 'workflows_task_instances_io'

	id = db.Column(db.Integer, primary_key=True)
	output_task_instance_id = db.Column(db.Integer, db.ForeignKey('workflows_tasks_instances.id'), nullable=False)
	output_task_file_id = db.Column(db.Integer, db.ForeignKey('tasks_output_files.id'), nullable=False)
	input_task_instance_id = db.Column(db.Integer, db.ForeignKey('workflows_tasks_instances.id'), nullable=False)
	input_task_file_id = db.Column(db.Integer, db.ForeignKey('tasks_input_files.id'), nullable=False)

	output_task_instance = db.relationship('WorkflowTaskInstance', foreign_keys=[output_task_instance_id], backref='outputs')
	input_task_instance = db.relationship('WorkflowTaskInstance', foreign_keys=[input_task_instance_id], backref='inputs')


class WorkflowJSONSerializer(JSONSerializer):
	__json_modifiers__ = {
		'tasks': lambda tasks, _: [dict(id=task.id) for task in tasks],
		'events': lambda events, _: [dict(id=event.id) for event in events],
		'revisions': lambda revisions, _: [dict(id=workflow.id) for revision in revisions],
		'task_instances': lambda task_instances, _: [dict(id=task.id) for task in task_instances]
		# add others here
	}


class Workflow(WorkflowJSONSerializer, db.Model):
	__tablename__ = 'workflows'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.Text, index=False, unique=False)
	revision = db.Column(db.Integer, nullable=False, default=0)
	revised_from_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	events = db.relationship('Event', backref='workflow', lazy='dynamic')
	revisions = db.relationship('Workflow', backref=db.backref('revised_from', remote_side=id), lazy='dynamic')
	task_instances = db.relationship('WorkflowTaskInstance', backref='workflow', lazy='dynamic')


	def __repr__(self):
		return '<Workflow %r>' % (self.name)
