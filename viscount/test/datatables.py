import unittest
import os.path

from viscount import app
from viscount.database import db, init_defaults, init_samples

from viscount.user import User

class DataTablesTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://viscount:viscountRocks@localhost/viscount_test'
		self.app = app.test_client()
		db.drop_all()
		db.create_all()
		init_defaults()
		init_samples()
		self.login('admin', 'admin')

	def tearDown(self):
		self.logout('admin', 'admin')
		db.session.remove()
		db.drop_all()

	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username=username,
			password=password
		), follow_redirects=True)
	
	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	# test cases
	def test_datatablesRequest(self):
		assert True

suite = unittest.TestLoader().loadTestsFromTestCase(DataTablesTests)
