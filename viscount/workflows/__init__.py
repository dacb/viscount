"""
viscount.workflows

provides workflow related services
"""

from ..core import Service
from .models import Workflow

class WorkflowsService(Service):
	__model__ = Workflow

	def add_task(self, workflow, task):
		if task in workflow.tasks:
			raise OverholtError(u'Task exists')
		workflow.tasks.append(task)
		return self.save(workflow)

	def remove_task(self, workflow, task):
		if task not in workflow.tasks:
			raise OverholtError(u'Invalid task')
		workflow.tasks.remove(task)
		return self.save(workflow)
