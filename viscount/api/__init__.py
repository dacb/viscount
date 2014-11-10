"""
viscount.api

provides the framework for the REST api
"""

from functools import wraps

from flask import jsonify
from flask.ext.security.decorators import login_required, roles_required

from ..core import ViscountException, ViscountFormException
from .datatables import DataTablesException, handle_DataTablesException
from .cytoscape import CytoscapeException, handle_CytoscapeException
from ..utils import JSONEncoder
from .. import factory


def create_app(config_override=None, register_security_blueprint=False):
	"""Returns the Viscount REST API application instance"""

	app = factory.create_app(__name__, __path__, config_override, register_security_blueprint=register_security_blueprint)

	# Set the default JSON encoder
	app.json_encoder = JSONEncoder

	# Register custom error handlers
	app.errorhandler(ViscountException)(handle_ViscountException)
	app.errorhandler(ViscountFormException)(handle_ViscountFormException)
	app.errorhandler(DataTablesException)(handle_DataTablesException)
	app.errorhandler(CytoscapeException)(handle_CytoscapeException)
	app.errorhandler(404)(handle_404)
	app.errorhandler(500)(handle_500)

	return app

# define all routes, enforce valid login
def route(bp, *args, **kwargs):
	kwargs.setdefault('strict_slashes', False)

	def decorator(f):
		@bp.route(*args, **kwargs)
		@login_required
		@wraps(f)
		def wrapper(*args, **kwargs):
			sc = 200
			rv = f(*args, **kwargs)
			if isinstance(rv, tuple):
				sc = rv[1]
				rv = rv[0]
			return jsonify(rv), sc
		return f

	return decorator

# error handlers
def handle_ViscountException(e):
	return jsonify(dict(error=e.message)), 400

def handle_ViscountFormException(e):
	return jsonify(dict(errors=e.errors)), 400

def handle_404(e):
	return jsonify(dict(error='Not found')), 404

def handle_500(e):
	return jsonify(dict(error='Internal server error')), 500
