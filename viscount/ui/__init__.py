"""
viscount.ui

application package for the user interface
"""

from functools import wraps

from flask import render_template
from flask_security import login_required

from ..utils import JSONEncoder
from .. import factory


def create_app(config_override=None):
	"""Returns the viscount UI application instance"""
	app = factory.create_app(__name__, __path__, config_override)

	# Set the default JSON encoder
	app.json_encoder = JSONEncoder

	# Set the error handler for DataTables exceptions

	return app


def route(bp, *args, **kwargs):
	def decorator(f):
		@bp.route(*args, **kwargs)
		@login_required
		@wraps(f)
		def wrapper(*args, **kwargs):
			return f(*args, **kwargs)
		return f

	return decorator


