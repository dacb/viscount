import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db
from .user import User

class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
	worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
	type = db.Column(db.Enum('created', 'modified', 'deleted', 'accessed', 'login', 'logout', 'queued', 'started', 'finished', 'failed'), index=True)

	def __repr__(self):
		return '<Log %r>' % (self.id)

	def message(self):
		msg = []
		if self.worker is not None:
			msg.append('woker %d' % self.worker.id)
		if self.user is not None:
			msg.append('user %s' % self.user.username)
		if self.type is not None:
			msg.append(self.type)
		if self.project is not None:
			msg.append('project %s' % self.project.name)
		if self.file is not None:
			msg.append('file %s' % self.file.filename)
		return ' : '.join(msg)

def logEntry(type, user=None, timestamp=datetime.datetime.utcnow(), project=None, file=None):
	user_id = None
	project_id = None
	file_id = None
	if user is not None:
		user_id = user.id
	if project is not None:
		project_id = project.id
	if file is not None:
		file_id = file.id
	entry = Log(user_id=user_id, timestamp=timestamp, project_id=project_id, file_id=file_id, type=type)
	db.session.add(entry)
	db.session.commit()
