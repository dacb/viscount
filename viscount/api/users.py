"""
viscount.api.users

User related endpoints
"""

from flask import Blueprint, request

from ..forms import NewUserForm, UpdateUserForm
from ..services import users as _users
from . import ViscountFormException, route

bp = Blueprint('users', __name__, url_prefix='/users')


@route(bp, '/')
def list():
	"""Returns a list of _user instances."""
	return _users.all()


@route(bp, '/<user_id>')
def show(user_id):
	"""Returns a _user instance."""
	return _users.get_or_404(user_id)


@route(bp, '/<workflow_id>', methods=['PUT'])
def update(workflow_id):
	"""Updates a workflow. Returns the updated workflow instance."""
	form = UpdateWorkflowForm()
	if form.validate_on_submit():
		return workflows.update(workflows.get_or_404(workflow_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<job_id>', methods=['DELETE'])
def delete(job_id):
	"""Deletes a job. Returns a 204 response."""
	_jobs.delete(jobs.get_or_404(job_id))
	return None, 204
