"""
viscount.workflows

provides workflow related services
"""

from ..core import Service
from .models import Workflow

class WorkflowsService(Service):
	__model__ = Workflow


	def create(self, **kwargs):
		"""Returns a new, saved instance of the workflow model class.

		:param **kwargs: instance parameters
		"""
		from ..services import events
		workflow = self.save(self.new(**kwargs))
		event = events.create(workflow_id=workflow.id, type='created', user_id=workflow.owner_id)
		return workflow


	def add_task(self, workflow, task):
		if task in workflow.tasks:
			raise ViscountError(u'Task exists')
		workflow.tasks.append(task)
		return self.save(workflow)


	def remove_task(self, workflow, task):
		if task not in workflow.tasks:
			raise ViscountError(u'Invalid task')
		workflow.tasks.remove(task)
		return self.save(workflow)
