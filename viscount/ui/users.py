from flask.ext.security.core import current_user
from flask import request, jsonify

from . import route
from ..models import User
from ..core import db
from .datatables import DataTables
from .index import bp


@route(bp, '/users',  methods = ['GET', 'POST'])
def users():
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
	return jsonify(rowTable.output_result())
