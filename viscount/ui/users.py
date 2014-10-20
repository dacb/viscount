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
		'username' : True,
		'lastName' : True,
		'firstName' : True,
		'email' : True,
		'isActive' : True,
		'last_login' : True,
		'current_login' : True,
		'last_login_ip' : True,
		'current_login_ip' : True,
		'login_count' : True,
		'role' : True,
	}
	query = db.session.query(User)
	rowTable = DataTables(request, User, query)
	return jsonify(rowTable.output_result())
