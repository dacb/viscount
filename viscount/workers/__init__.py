"""
viscount.workers

provides worker related services
"""

from ..core import Service
from .models import Worker

class WorkersService(Service):
	__model__ = Worker
