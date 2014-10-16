import unittest
import os.path

from viscount import app
from viscount.database import db, init_defaults, init_samples

class DatabaseTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['DATADIR'], 'test.db')
		self.app = app.test_client()
		db.create_all()
		init_defaults()
		init_samples()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# test cases
	def test_userEventRelationship(self):
		e4 = db.session.query(Event).get(4)
		u1 = db.session.query(User).get(1)
		assert e4.user == u1

suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTests)
