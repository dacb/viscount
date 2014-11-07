"""
viscount.api.users

User related endpoints
"""

from flask import Blueprint, request, jsonify

from ..forms import NewUserForm, UpdateUserForm
from ..services import users as _users
from . import ViscountFormException, ViscountException, route
from ..models import User
from ..core import db
from .datatables import DataTables


bp = Blueprint('users', __name__, url_prefix='/users')


@route(bp, '/')
def list():
	"""Returns a list of _user instances."""
	return _users.all()


@route(bp, '/', methods=['POST'])
def create():
	"""Creates a new _user. Returns the new _user instance."""
	form = NewUserForm()
	print form.data
	if form.validate_on_submit():
		if _users.find(email=form.data['email']).count() > 0:
			raise ViscountException(message="A user with that email already exists!")
		if _users.find(username=form.data['username']).count() > 0:
			raise ViscountException(message="A user with that username already exists!")
		return _users.create(**form.data)
	raise ViscountFormException(form.errors)


@route(bp, '/<user_id>')
def show(user_id):
	"""Returns a _user instance."""
	return _users.get_or_404(user_id)


@route(bp, '/<user_id>', methods=['PUT'])
def update(user_id):
	"""Updates a user. Returns the updated user instance."""
	form = UpdateUserForm()
	if form.validate_on_submit():
		return users.update(users.get_or_404(user_id), **request.json)
	raise(ViscountFormException(form.errors))


@route(bp, '/<user_id>', methods=['DELETE'])
def delete(user_id):
	"""Deletes a user. Returns a 204 response."""
	_users.delete(users.get_or_404(user_id))
	return None, 204


@route(bp, '/datatables',  methods = ['GET', 'POST'])
def datatables():
	column_whitelist = {
		'id' : True,
		'email' : True,
		'username' : True,
		'lastName' : True,
		'firstName' : True,
		'active' : True,
		'confirmed_at' : True,
		'last_login_at' : True,
		'current_login_at' : True,
		'last_login_ip' : True,
		'current_login_ip' : True,
		'login_count' : True,
		'registered_at' : True,
		'roles' : True,
	}
	query = db.session.query(User)
	rowTable = DataTables(request, User, query, column_whitelist)
	return rowTable.output_result(), 200
