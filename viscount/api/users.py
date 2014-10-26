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


@route(bp, '/', methods=['POST'])
def create():
	"""Creates a new _user. Returns the new _user instance."""
	form = NewUserForm()
	print form.data
	if form.validate_on_submit():
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
