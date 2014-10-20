"""
viscount.projects

provides project related services
"""

from ..core import Service, db
from .models import Project

class ProjectsService(Service):
	__model__ = Project

	def create(self, **kwargs):
		"""Returns a new, saved instance of the project model class.

		:param **kwargs: instance parameters
		"""
		from ..services import events
		project = self.save(self.new(**kwargs))
		event = events.create(project_id=project.id, type='created')
		return project
