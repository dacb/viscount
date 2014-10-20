"""
viscount.events

provides event related services
"""

from ..core import Service
from .models import Event


class EventsService(Service):
	__model__ = Event
