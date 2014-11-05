import os
from flask import Blueprint, render_template, session, current_app
from flask_wtf import Form
from flask.ext.security.core import current_user

from . import route
from ..services import roles as _roles

bp = Blueprint('ui', __name__)


@route(bp, '/')
def index():
	"""Returns the main index page for the ui"""
	print current_app.config['INCOMING_DIR']
	print os.listdir(current_app.config['INCOMING_DIR'])
	available_files = os.listdir(current_app.config['INCOMING_DIR'])
	return render_template("index.html", title='Home', user=current_user, roles=_roles.all(), available_files=available_files)
