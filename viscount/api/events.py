"""
viscount.api.events

Event related endpoints
"""

from flask import Blueprint, request, jsonify

from ..services import events as _events
from . import route
from ..models import Event, User, Project, File, Workflow
from ..core import db
from .datatables import DataTables


bp = Blueprint('events', __name__, url_prefix='/events')


@route(bp, '/')
def list():
	"""Returns a list of event instances."""
	return _events.all()


@route(bp, '/<event_id>')
def show(event_id):
	"""Returns a event instance."""
	return _events.get_or_404(event_id)


@route(bp, '/datatables',  methods = ['GET', 'POST'])
def datatables():
	column_whitelist = {
		'id' : True,
		'user_id' : True,
		'user.username' : True,
		'timestamp' : True,
		'project_id' : True,
		'project.name' : True,
		'file_id' : True,
		'file.filename' : True,
		'workflow_id' : True,
		'workflow.filename' : True,
		'job_id' : True,
		'worker_id' : True,
		'type' : True,
	}
	query = db.session.query(Event). \
		outerjoin(User, (User.id == Event.user_id)). \
		outerjoin(Project, (Project.id == Event.project_id)). \
		outerjoin(File, (File.id == Event.file_id)). \
		outerjoin(Workflow, (Workflow.id == Event.workflow_id))
	rowTable = DataTables(request, Event, query)
	return rowTable.output_result(), 200
