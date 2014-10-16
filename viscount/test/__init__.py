from flask.ext.script import Manager, Server, Shell
import unittest

from viscount import app
from viscount.database import db

manager = Manager(app, usage="Test harness for viscount", with_default_commands=False)

@manager.command
def run(db=False, stub=False, loginout=False, tables=False, all=True):
	suite = unittest.TestSuite()

	if db or stub or loginout or tables:
		all = False
	if db or all:
		from viscount.test.database import suite as database_suite
		suite.addTest(database_suite)
	if loginout or all:
		from viscount.test.loginout import suite as loginout_suite
		suite.addTest(loginout_suite)
	if tables or all:
		from viscount.test.datatables import suite as datatables_suite
		suite.addTest(datatables_suite)
	if stub or all:
		from viscount.test.stub import suite as stub_suite
		suite.addTest(stub_suite)

	unittest.TextTestRunner(verbosity=2).run(suite)
