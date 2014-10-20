"""
viscount.workflows

provides workflow related services
"""

from ..core import Service, db
from .models import User, Role


class UsersService(Service):
	__model__ = User

	def create(self, **kwargs):
		"""Returns a new, saved instance of the user model class.

		:param **kwargs: instance parameters
		"""
		from ..services import events
		user = self.save(self.new(**kwargs))
		event = events.create(user_id=user.id, type='created')
		return user


class RolesService(Service):
	__model__ = Role
