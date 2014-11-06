from flask.ext.security.core import current_user
from flask import request, jsonify

from . import route
from ..models import Event, User, Project, File, Workflow
from ..core import db
from .datatables import DataTables
from .index import bp


@route(bp, '/events',  methods = ['GET', 'POST'])
def events():
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
	return jsonify(rowTable.output_result())
