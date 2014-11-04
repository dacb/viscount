"""
viscount.api.files

File related endpoints
"""

from flask import Blueprint, request

from ..forms import NewFileForm, UpdateFileForm
from ..services import files as _files
from . import ViscountFormException, route

bp = Blueprint('files', __name__, url_prefix='/files')


@route(bp, '/')
def list():
	"""Returns a list of file instances."""
	return _files.all()


@route(bp, '/', methods=['POST'])
def create():
	"""Creates a new file. Returns the new file instance."""
	form = NewFileForm()
	if form.validate_on_submit():
		return _files.create(**form.data)
	raise ViscountFormException(form.errors)


@route(bp, '/<file_id>')
def show(file_id):
	"""Returns a file instance."""
	return _files.get_or_404(file_id)


@route(bp, '/<file_id>', methods=['PUT'])
def update(file_id):
	"""Updates a file. Returns the updated file instance."""
	form = UpdateFileForm()
	if form.validate_on_submit():
		return _files.update(files.get_or_404(file_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<file_id>', methods=['DELETE'])
def delete(file_id):
	"""Deletes a file. Returns a 204 response."""
	_files.delete(files.get_or_404(file_id))
	return None, 204
