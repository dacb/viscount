"""
viscount ui app test cases

includes tests for testing authentication
"""

from . import ViscountUITestCase


class IndexTestCase(ViscountUITestCase):

	def test_auth(self):
		r = self.get('/')
		self.assertOk(r)
		self.assertIn('<h1>Index</h1>', r.data)

	def test_unauth(self):
		self.get('/logout')
		r = self.get('/')
		self.assertOk(r)
		self.assertNotIn('<h1>Index</h1>', r.data)
