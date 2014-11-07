"""
viscount.api.workflows

Workflow related endpoints
"""

from flask import Blueprint, request, jsonify

from ..forms import NewWorkflowForm, UpdateWorkflowForm
from ..services import workflows as _workflows, tasks as _tasks
from . import ViscountFormException, route
from ..models import Workflow
from ..core import db
from .datatables import DataTables


bp = Blueprint('workflows', __name__, url_prefix='/workflows')


@route(bp, '/')
def list():
	"""Returns a list of workflow instances."""
	return _workflows.all()


@route(bp, '/', methods=['POST'])
def create():
	"""Creates a new workflow. Returns the new workflow instance."""
	form = NewWorkflowForm()
	if form.validate_on_submit():
		return _workflows.create(**request.json)
	raise ViscountFormException(form.errors)


@route(bp, '/<workflow_id>')
def show(workflow_id):
	"""Returns a workflow instance."""
	return _workflows.get_or_404(workflow_id)


@route(bp, '/<workflow_id>', methods=['PUT'])
def update(workflow_id):
	"""Updates a workflow. Returns the updated workflow instance."""
	form = UpdateWorkflowForm()
	if form.validate_on_submit():
		return _workflows.update(_workflows.get_or_404(workflow_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<workflow_id>', methods=['DELETE'])
def delete(workflow_id):
	"""Deletes a workflow. Returns a 204 response."""
	_workflows.delete(_workflows.get_or_404(workflow_id))
	return None, 204


@route(bp, '/<workflow_id>/tasks')
def tasks(workflow_id):
	"""Returns a list of task instances belonging to a workflow."""
	return _workflows.get_or_404(workflow_id).tasks


@route(bp, '/<workflow_id>/tasks/<task_id>', methods=['PUT'])
def add_task(workflow_id, task_id):
	"""Adds a task to a workflow. Returns the task instance."""
	return _workflows.add_task(_workflows.get_or_404(workflow_id), _tasks.get_or_404(task_id))


@route(bp, '/<workflow_id>/tasks/<task_id>', methods=['DELETE'])
def remove_task(workflow_id, task_id):
	"""Removes a task form a workflow. Returns a 204 response."""
	_workflows.remove_task(_workflows.get_or_404(workflow_id), _tasks.get_or_404(task_id))
	return None, 204


@route(bp, '/datatables', methods=['GET', 'POST'])
def datatables():
	column_whitelist = {
		"id" : True,
		"name" : True,
		"description" : True,
		"revision" : True,
		"revised_from.id" : True,
		"revised_from.name" : True,
		"revised_from.description" : True,
		"revised_from.revision" : True
	}
	query = db.session.query(Workflow)
	rowTable = DataTables(request, Workflow, query, column_whitelist)
	return rowTable.output_result(), 200
