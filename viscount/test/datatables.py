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
		self.logout()
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
		rv = self.app.post('/events', data={
			"columns[8][data]" : "",
			"columns[4][search][regex]" : "false",
			"columns[4][orderable]" : "true",
			"columns[5][orderable]" : "true",
			"columns[2][orderable]" : "true",
			"order[0][dir]" : "desc",
			"columns[6][searchable]" : "true",
			"order[3][column]" : "5",
			"columns[3][name]" : "",
			"columns[0][search][regex]" : "false",
			"start" : "0",
			"columns[5][search][value]" : "",
			"columns[3][searchable]" : "true",
			"columns[8][orderable]" : "false",
			"columns[2][search][regex]" : "false",
			"columns[5][search][regex]" : "false",
			"columns[0][orderable]" : "true",
			"columns[4][data]" : "file_id",
			"columns[0][name]" : "",
			"columns[3][data]" : "project_id",
			"search[value]" : "",
			"order[2][column]" : "4",
			"columns[6][search][regex]" : "false",
			"search[regex]" : "false",
			"columns[6][search][value]" : "",
			"columns[7][data]" : "type",
			"columns[8][search][regex]" : "false",
			"columns[3][search][value]" : "",
			"draw" : "1",
			"columns[0][data]" : "id",
			"order[1][dir]" : "asc",
			"columns[1][name]" : "",
			"columns[5][searchable]" : "true",
			"columns[5][name]" : "",
			"columns[1][orderable]" : "true",
			"order[0][column]" : "3",
			"columns[2][search][value]" : "",
			"columns[4][name]" : "",
			"columns[1][search][regex]" : "false",
			"columns[7][search][value]" : "",
			"columns[6][name]" : "",
			"columns[2][searchable]" : "true",
			"columns[3][search][regex]" : "false",
			"columns[7][searchable]" : "true",
			"columns[7][name]" : "",
			"columns[0][search][value]" : "",
			"columns[4][searchable]" : "true",
			"columns[7][search][regex]" : "false",
			"columns[8][name]" : "",
			"columns[0][searchable]" : "true",
			"order[2][dir]" : "asc",
			"order[3][dir]" : "asc",
			"columns[7][orderable]" : "true",
			"columns[5][data]" : "job_id",
			"columns[8][searchable]" : "true",
			"columns[1][data]" : "user\.username",
			"columns[1][searchable]" : "true",
			"columns[2][data]" : "timestamp",
			"columns[8][search][value]" : "",
			"columns[3][orderable]" : "true",
			"columns[6][data]" : "worker_id",
			"order[1][column]" : "2",
			"columns[4][search][value]" : "",
			"columns[6][orderable]" : "true",
			"columns[1][search][value]" : "",
			"columns[2][name]" : "",
			"length" : "10",
		}, follow_redirects=True)
		assert 'data' in rv.data

suite = unittest.TestLoader().loadTestsFromTestCase(DataTablesTests)
