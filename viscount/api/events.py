"""
viscount.api.events

Event related endpoints
"""

from flask import Blueprint, request

from ..services import events as _events
from . import route

bp = Blueprint('events', __name__, url_prefix='/events')


@route(bp, '/')
def list():
	"""Returns a list of event instances."""
	return _events.all()


@route(bp, '/<event_id>')
def show(event_id):
	"""Returns a event instance."""
	return _events.get_or_404(event_id)
