"""
viscount.api.workers

Worker related endpoints
"""

from flask import Blueprint, request

from ..forms import NewWorkerForm, UpdateWorkerForm
from ..services import workers as _workers
from . import ViscountFormException, route

bp = Blueprint('workers', __name__, url_prefix='/workers')


@route(bp, '/')
def list():
	"""Returns a list of _worker instances."""
	return _workers.all()


@route(bp, '/<worker_id>')
def show(worker_id):
	"""Returns a _worker instance."""
	return _workers.get_or_404(worker_id)


@route(bp, '/<worker_id>', methods=['PUT'])
def update(worker_id):
	"""Updates a _worker. Returns the updated _worker instance."""
	form = UpdateWorkerForm()
	if form.validate_on_submit():
		return _workers.update(workers.get_or_404(worker_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<worker_id>', methods=['DELETE'])
def delete(worker_id):
	"""Deletes a _worker. Returns a 204 response."""
	_workers.delete(workers.get_or_404(worker_id))
	return None, 204

