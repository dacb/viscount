"""
viscount.api.files

File related endpoints
"""

from flask import Blueprint, request, jsonify

from ..forms import NewFileForm, UpdateFileForm
from ..services import files as _files
from . import ViscountFormException, route
from ..models import File, User
from ..core import db
from .datatables import DataTables


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


@route(bp, '/datatables',  methods = ['GET', 'POST'])
def datatables():
	column_whitelist = {
		"id" : True,
		"filename" : True,
		"user.username" : True,
		"description" : True,
		"md5sum" : True
	}
	query = db.session.query(File). \
		outerjoin(User, (User.id == File.owner_id))
	rowTable = DataTables(request, File, query)
	return rowTable.output_result(), 200
