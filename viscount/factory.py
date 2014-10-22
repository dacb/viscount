"""
viscount.factor

app factory
"""

import os

from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .core import db, security #, csrf
from .utils import register_blueprints
from .users.models import User, Role


def create_app(package_name, package_path, config_override=None, register_security_blueprint=True):
	"""Returns a :class:`Flask` application instance configured with common
	functionality for the Overholt platform.

	:param package_name: application package name
	:param package_path: application package path
	:param config_override: a dictionary of config to override
	:param register_security_blueprint: flag to specify if the Flask-Security
										Blueprint should be registered. Defaults
										to `True`.
	"""
	app = Flask(package_name, instance_relative_config=True)

	app.config.from_object('config.Config')
	app.config.from_object(config_override)

	db.init_app(app)
	security.init_app(app, SQLAlchemyUserDatastore(db, User, Role), register_blueprint=register_security_blueprint)
#	csrf.init_app(app)

	register_blueprints(app, package_name, package_path)

	return app
