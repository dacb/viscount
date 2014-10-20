"""
viscount.api.tasks

Task related endpoints
"""

from flask import Blueprint, request

from ..forms import NewTaskForm, UpdateTaskForm
from ..services import tasks as _tasks
from . import ViscountFormException, route

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@route(bp, '/')
def list():
	"""Returns a list of _task instances."""
	return _tasks.all()


@route(bp, '/', methods=['POST'])
def create():
	"""Creates a new _task. Returns the new _task instance."""
	form = NewTaskForm()
	if form.validate_on_submit():
		return _tasks.create(**request.json)
	raise ViscountFormException(form.errors)


@route(bp, '/<task_id>')
def show(task_id):
	"""Returns a _task instance."""
	return _tasks.get_or_404(task_id)


@route(bp, '/<task_id>', methods=['PUT'])
def update(task_id):
	"""Updates a _task. Returns the updated _task instance."""
	form = UpdateTaskForm()
	if form.validate_on_submit():
		return _tasks.update(tasks.get_or_404(task_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<task_id>', methods=['DELETE'])
def delete(task_id):
	"""Deletes a _task. Returns a 204 response."""
	_tasks.delete(tasks.get_or_404(task_id))
	return None, 204
