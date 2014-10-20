"""
viscount.files

provides file related services
"""

from ..core import Service
from .models import File

class FilesService(Service):
	__model__ = File
