"""
viscount REST API workflow test unit

tests get, create, update, delete for workflows
and task relationships for a workflow
"""

from ..factories import WorkflowFactory, TaskFactory
from . import ViscountApiTestCase


class WorkflowApiTestCase(ViscountApiTestCase):

	def _create_fixtures(self):
		super(WorkflowApiTestCase, self)._create_fixtures()
		self.task = TaskFactory()
		self.workflow = WorkflowFactory(tasks=[self.task])

	def test_get_workflows(self):
		r = self.jget('/workflows')
		self.assertOkJson(r)

	def test_get_workflow(self):
		r = self.jget('/workflows/%s' % self.workflow.id)
		self.assertOkJson(r)

	def test_create_workflow(self):
		r = self.jpost('/workflows', data={
			'name': 'Example Workflow',
			'description': 'Sample workflow for testing',
		})
		self.assertOkJson(r)
		self.assertIn('"name": "Example Workflow"', r.data)

	def test_create_invalid_workflow(self):
		r = self.jpost('/workflows', data={
			'name': 'Example Workflow',
			'csrf_token': self.csrf_token
		})
		self.assertBadJson(r)
		self.assertIn('"errors": {', r.data)

	def test_update_workflow(self):
		r = self.jput('/workflows/%s' % self.workflow.id, data={
			'name': 'Example Workflow Renamed'
		})
		self.assertOkJson(r)
		self.assertIn('"name": "Example Workflow Renamed"', r.data)

	def test_delete_workflow(self):
		r = self.jdelete('/workflows/%s' % self.workflow.id)
		self.assertStatusCode(r, 204)

	def test_get_tasks(self):
		r = self.jget('/workflows/%s/tasks' % self.workflow.id)
		self.assertOkJson(r)

	def test_add_task(self):
		p = TaskFactory()
		e = '/workflows/%s/tasks/%s' % (self.workflow.id, p.id)
		r = self.jput(e)
		self.assertOkJson(r)

	def test_remove_task(self):
		e = '/workflows/%s/tasks/%s' % (self.workflow.id, self.task.id)
		r = self.jdelete(e)
		self.assertStatusCode(r, 204)
