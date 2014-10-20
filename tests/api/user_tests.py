"""
viscount REST API users blueprint tests
"""

from . import ViscountApiTestCase


class UserApiTestCase(ViscountApiTestCase):

	def test_getUsers(self):
		r = self.jget('/users')
		self.assertOkJson(r)

	def test_getUser(self):
		r = self.jget('/users/%s' % self.user.id)
		self.assertOkJson(r)
