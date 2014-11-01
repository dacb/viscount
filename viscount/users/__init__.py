"""
viscount.workflows

provides workflow related services
"""

from ..core import Service, db
from .models import User, Role
from datetime import datetime


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

	def new(self, **kwargs):
		"""Returns a new, unsaved instance of the service's model class.

		:param **kwargs: instance parameters
		"""
		kwargs.update({'confirmed_at' : datetime.utcnow(), 'registered_at' : datetime.utcnow(), 'active' : True, 'login_count' : 0})
		return self.__model__(**self._preprocess_params(kwargs))


class RolesService(Service):
	__model__ = Role
