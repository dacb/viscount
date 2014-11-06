from flask.ext.security.core import current_user
from flask import request, jsonify

from . import route
from ..models import Workflow, User
from ..core import db
from .datatables import DataTables
from .index import bp


@route(bp, '/workflows',  methods = ['GET', 'POST'])
def workflows():
	column_whitelist = {
		"id" : True,
		"name" : True,
		"description" : True,
		"revision" : True,
		"revised_from.name" : True,
		"revised_from.description" : True,
		"revised_from.revision" : True,
	}
	query = db.session.query(Workflow)
	rowTable = DataTables(request, Workflow, query, column_whitelist)
	return jsonify(rowTable.output_result())
