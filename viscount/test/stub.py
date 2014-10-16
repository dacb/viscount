#!venv/bin/python
import unittest

from viscount import app
from viscount.database import db, init_defaults, init_sample

class SuiteTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()
		init_defaults()
		init_sample()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# test cases
	def test_stubeExample(self):
		assert 1 == 1

suite = unittest.TestLoader().loadTestsFromTestCase(SuiteTests)