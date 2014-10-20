"""
viscout UI unit test case

class for dispatching all viscount UI tasks
"""

from viscount.ui import create_app

from .. import ViscountAppTestCase


class ViscountUITestCase(ViscountAppTestCase):

	def _create_app(self):
		return create_app(config.ConfigTesting)

	def setUp(self):
		super(ViscountUITestCase, self).setUp()
		self._login()
