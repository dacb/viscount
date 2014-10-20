from flask.ext.security.core import current_user
from flask import request, jsonify

from . import route
from ..models import Project, User
from ..core import db
from .datatables import DataTables
from .index import bp


@route(bp, '/projects',  methods = ['GET', 'POST'])
def projects():
	column_whitelist = {
		"id" : True,
		"name" : True,
		"owner_id" : True,
		"owner.username" : True,
		"description" : True,
	}
	query = db.session.query(Project). \
		outerjoin(User, (User.id == Project.owner_id))
	rowTable = DataTables(request, Project, query, column_whitelist)
	print jsonify(rowTable.output_result()).data
	return jsonify(rowTable.output_result())
