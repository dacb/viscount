"""
viscount.api.projects

Project related endpoints
"""

from flask import Blueprint, request, jsonify

from ..forms import NewProjectForm, UpdateProjectForm
from ..services import projects as _projects
from . import ViscountFormException, route
from ..models import Project, User
from ..core import db
from .datatables import DataTables


bp = Blueprint('projects', __name__, url_prefix='/projects')


@route(bp, '/')
def list():
	"""Returns a list of _project instances."""
	return _projects.all()


@route(bp, '/', methods=['POST'])
def create():
	"""Creates a new _project. Returns the new _project instance."""
	form = NewProjectForm()
	if form.validate_on_submit():
		return _projects.create(**request.json)
	raise ViscountFormException(form.errors)


@route(bp, '/<project_id>')
def show(project_id):
	"""Returns a _project instance."""
	return _projects.get_or_404(project_id)


@route(bp, '/<project_id>', methods=['PUT'])
def update(project_id):
	"""Updates a _project. Returns the updated _project instance."""
	form = UpdateProjectForm()
	if form.validate_on_submit():
		return _projects.update(projects.get_or_404(project_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<project_id>', methods=['DELETE'])
def delete(project_id):
	"""Deletes a _project. Returns a 204 response."""
	_projects.delete(projects.get_or_404(project_id))
	return None, 204


@route(bp, '/datatables',  methods = ['GET', 'POST'])
def datatables():
	column_whitelist = {
		"id" : True,
		"name" : True,
		"owner_id" : True,
		"owner.username" : True,
		"description" : True,
	}
	query = db.session.query(Project). \
		outerjoin(User, (User.id == Project.owner_id))
	rowTable = DataTables(request, Project, query, column_whitelist)
	return rowTable.output_result(), 200
