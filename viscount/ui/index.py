from flask import Blueprint, render_template, session
from flask_wtf import Form
from flask.ext.security.core import current_user

from . import route
from ..services import roles as _roles

bp = Blueprint('ui', __name__)


@route(bp, '/')
def index():
	"""Returns the main index page for the ui"""
	return render_template("index.html", title='Home', user=current_user, roles=_roles.all(), csrf_token=session['csrf_token'])
