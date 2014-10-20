"""
viscount REST API unit test class
"""

from viscount.api import create_app

from .. import ViscountAppTestCase
import config

class ViscountApiTestCase(ViscountAppTestCase):

	def _create_app(self):
		app = create_app(config.TestingConfig, register_security_blueprint=True)
		return app

	def setUp(self):
		super(ViscountApiTestCase, self).setUp()
		self._login()
