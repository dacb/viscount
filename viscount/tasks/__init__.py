"""
viscount.tasks

provides task related services
"""

from ..core import Service
from .models import TaskInputFile, TaskOutputFile, Task

class TaskInputFilesService(Service):
	__model__ = TaskInputFile


class TaskOutputFilesService(Service):
	__model__ = TaskOutputFile


class TasksService(Service):
	__model__ = Task
