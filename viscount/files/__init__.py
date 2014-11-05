"""
viscount.files

provides file related services
"""

from flask_security.core import current_user


from ..core import Service
from .models import FileType, File

class FilesService(Service):
	__model__ = File

	def create(self, **kwargs):
		"""Returns a new, saved instance of the file model class.

		:param **kwargs: instance parameters
		"""
		from ..services import events
		file = self.save(self.new(**kwargs))
		event = events.create(file_id=file.id, user_id=current_user.id, type='created')
		return file

	def new(self, **kwargs):
		"""Returns a new, unsaved instance of the service's model class.

		:param **kwargs: instance parameters
		"""
		kwargs.update({'user_id' : current_user.id })
		return self.__model__(**self._preprocess_params(kwargs))


class FileTypesService(Service):
	__model__ = FileType
