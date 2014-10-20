from flask.ext.security.core import current_user
from flask import request, jsonify

from . import route
from ..models import File, User
from ..core import db
from .datatables import DataTables
from .index import bp


@route(bp, '/files',  methods = ['GET', 'POST'])
def files():
	column_whitelist = {
		"id" : True,
		"filename" : True,
		"user.username" : True,
		"description" : True,
		"md5sum" : True
	}
	query = db.session.query(File). \
		outerjoin(User, (User.id == File.user_id))
	rowTable = DataTables(request, File, query)
	return jsonify(rowTable.output_result())
