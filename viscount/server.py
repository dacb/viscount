import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from .json import custom_json_output

app = Flask("viscount")
app.config.from_object('config')
db = SQLAlchemy(app)

# flask-restful setup
class BadRequestError(ValueError):
	status_code = 400
	message = 'Request was bad'

class ExceptionAwareApi(Api):
	def handle_error(self, e):
		if issubclass(e.__class__, BadRequestError):
			code = e.status_code
			data = { 'status_code': code, 'message': e.message }
		else:
			# Did not match a custom exception, continue normally
			return super(ExceptionAwareApi, self).handle_error(e)
		return self.make_response(data, code)

api = ExceptionAwareApi(app)
# now use our custom_json_converter that handles datetime
api.representations.update({
	'application/json': custom_json_output
})

from viscount import user, views, project, event, file, job, worker

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
