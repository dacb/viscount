"""
viscount main driver

leverages flask-script to provide a management interface to a
viscount installation

commands include database
"""

import os.path
from flask.ext.script import Manager

from viscount import api

app = api.create_app()
manager = Manager(app)

# include database manager
from .database import manager as database_manager
manager.add_command("database", database_manager)
