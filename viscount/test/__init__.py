from flask.ext.script import Manager, Server, Shell
import unittest

#
# in accordance with the following, tests should be named:
# test_HelpfulTestName_X_Y
# where X and Y are numbers, tests will be sorted by X first and if equal then Y
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: cmp(int(x.rsplit('_', 2)[1]), int(y.rsplit('_', 2)[1])) if cmp(int(x.rsplit('_', 2)[1]), int(y.rsplit('_', 2)[1])) != 0 else cmp(int(x.rsplit('_', 1)[1]), int(y.rsplit('_', 1)[1]));
#

# 
# this overides the default unittest runner to stop on any previous failures or errors
# note the abort happens on the run of the next failed test case
def aborting_run(self, result=None):
    if result.failures or result.errors:
        print "aborted"
    else:
        original_run(self, result)
original_run = unittest.TestCase.run
unittest.TestCase.run = aborting_run
#

from viscount import app
from viscount.database import db

manager = Manager(app, usage="Test harness for viscount", with_default_commands=False)

@manager.command
def run(db=False, stub=False, loginout=False, tables=False, all=True, continueOnFail=False):
	"Runs the test, required command"
	suite = unittest.TestSuite()

	if continueOnFail:
		unittest.TestCase.run = original_run

	if db or stub or loginout or tables:
		all = False
	if stub or all:
		from viscount.test.stub import suite as stub_suite
		suite.addTest(stub_suite)
	if db or all:
		from viscount.test.database import suite as database_suite
		suite.addTest(database_suite)
	if loginout or all:
		from viscount.test.loginout import suite as loginout_suite
		suite.addTest(loginout_suite)
	if tables or all:
		from viscount.test.datatables import suite as datatables_suite
		suite.addTest(datatables_suite)

	unittest.TextTestRunner(verbosity=2).run(suite)
