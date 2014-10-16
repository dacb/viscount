from flask.ext.script import Manager, Server, Shell
import unittest

from viscount import app
from viscount.database import db

manager = Manager(app, usage="Test harness for viscount", with_default_commands=False)

suite = unittest.TestSuite()

@manager.command
def run(db=False, stub=False, all=True):
	if db or stub:
		all = False
	if db or all:
		from viscount.test.database import suite as database_suite
		suite.addTest(database_suite)
	if stub or all:
		from viscount.test.stub import suite as stub_suite
		suite.addTest(stub_suite)
	unittest.TextTestRunner(verbosity=2).run(suite)
