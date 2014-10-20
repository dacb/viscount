"""
viscount.jobs

provides job related services
"""

from ..core import Service
from .models import Job

class JobsService(Service):
	__model__ = Job
