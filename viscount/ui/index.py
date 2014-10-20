from flask import Blueprint, render_template
from flask.ext.security.core import current_user

from . import route

bp = Blueprint('ui', __name__)


@route(bp, '/')
def index():
	"""Returns the main index page for the ui"""
	return render_template("index.html", title='Home', user=current_user)
