"""
viscount unittests

contains a basic unit test class that can be used for all instances
"""

from unittest import TestCase

from viscount.core import db

from .factories import UserFactory
from .utils import FlaskTestCaseMixin


class ViscountTestCase(TestCase):
	pass


class ViscountAppTestCase(FlaskTestCaseMixin, ViscountTestCase):

	def _create_app(self):
		raise NotImplementedError

	def _create_fixtures(self):
		## expand
		self.user = UserFactory()

	def setUp(self):
		super(ViscountAppTestCase, self).setUp()
		self.app = self._create_app()
		self.client = self.app.test_client()
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.drop_all()
		db.create_all()
		self._create_fixtures()
		self._create_csrf_token()

	def tearDown(self):
		super(ViscountAppTestCase, self).tearDown()
		db.drop_all()
		self.app_context.pop()

	def _login(self, email=None, password=None):
		email = email or self.user.email
		password = password or 'password'
		ret = self.post('/login', data={'email': email, 'password': password}, follow_redirects=False)
		return ret
