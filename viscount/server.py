import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from .json import custom_json_output

app = Flask("viscount")
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)
# now use our custom_json_converter that handles datetime
api.representations.update({
	'application/json': custom_json_output
})

from viscount import user, views, project, log, file, job, worker

class Server():
	def __init__(self, host=None, port=None, debug=False, allowRoot=False):
		self._port = port
		self._host = host
		self._debug = debug
		self._allowRoot = allowRoot

	def run(self):
		if not self._allowRoot:
			self._checkForRoot()

		app.debug = self._debug

		app.run(host=self._host, port=self._port)

	def _checkForRoot(self):
		if "geteuid" in dir(os) and os.geteuid() == 0:
			exit("Do not run viscount as root!")
