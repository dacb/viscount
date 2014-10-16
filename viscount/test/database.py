import unittest
import os.path

from viscount import app
from viscount.database import db, init_defaults, init_samples

from viscount.user import User

class DatabaseTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['DATADIR'], 'test.db')
		self.app = app.test_client()
		db.drop_all()
		db.create_all()
		init_defaults()
		init_samples()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# test cases
	def test_userEventRelationship(self):
		from viscount.event import Event
		from viscount.user import User
		u1 = db.session.query(User).get(1)
		assert u1.username == 'admin'
		e1 = db.session.query(Event).get(1)
		assert e1.user_id == 1

suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTests)
