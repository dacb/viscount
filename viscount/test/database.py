import os.path

from viscount import app
from viscount.database import db, init_defaults, init_samples

from viscount.test import unittest

from viscount.user import User

class DatabaseTests(unittest.TestCase):
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
	def test_userEventRelationship_1_0(self):
		from viscount.event import Event
		from viscount.user import User
		u1 = db.session.query(User).get(1)
		assert u1.username == 'admin'
		e1 = db.session.query(Event).get(1)
		assert e1.user_id == None
		assert e1.user == None
		e2 = db.session.query(Event).get(2)
		assert e2.user_id == 1
		assert e2.user == u1

	def test_projectEventRelationship_1_1(self):
		from viscount.event import Event
		from viscount.project import Project
		p1 = db.session.query(Project).get(1)
		e5 = db.session.query(Event).get(5)
		assert e5.project == p1


suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTests)
