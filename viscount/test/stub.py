import os.path

from viscount import app
from viscount.database import db, init_defaults, init_samples

from viscount.test import unittest

class StubTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://viscount:viscountRocks@localhost/viscount_test'
		self.app = app.test_client()
		db.drop_all()
		db.create_all()
		init_defaults()
		init_samples()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# test cases
	def test_stubExample_0_0(self):
		assert 1 == 1

suite = unittest.TestLoader().loadTestsFromTestCase(StubTests)
