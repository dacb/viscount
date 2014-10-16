import os.path
from flask.ext.script import Manager, Server, Shell

from viscount import app
from viscount.database import db

manager = Manager(app, usage="Manage viscount server installation")

# add a default target
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))

# add the shell target
def _make_context():
	return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=_make_context))

# include database manager
from viscount.manage.database import manager as database_manager
manager.add_command("database", database_manager)
