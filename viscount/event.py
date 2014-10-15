import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db
from .user import User

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
	worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
	type = db.Column(db.Enum('created', 'modified', 'deleted', 'accessed', 'login', 'logout', 'queued', 'started', 'finished', 'failed'), index=True)

	def __repr__(self):
		return '<Event %r>' % (self.id)

	def message(self):
		msg = []
		if self.worker is not None:
			msg.append('woker %d' % self.worker.id)
		if self.job is not None:
			msg.append('job %d' % self.job.id)
		if self.user is not None:
			msg.append('user %s' % self.user.username)
		if self.type is not None:
			msg.append(self.type)
		if self.project is not None:
			msg.append('project %s' % self.project.name)
		if self.file is not None:
			msg.append('file %s' % self.file.filename)
		return ' : '.join(msg)

def eventEntry(type, user=None, timestamp=datetime.datetime.utcnow(), project=None, file=None, job=None):
	user_id = None
	project_id = None
	file_id = None
	job_id = None
	worker_id = None
	if user is not None:
		user_id = user.id
	if project is not None:
		project_id = project.id
	if file is not None:
		file_id = file.id
	if job is not None:
		job_id = job.id
	entry = Event(user_id=user_id, timestamp=timestamp, project_id=project_id, file_id=file_id, type=type, job_id=job_id, worker_id=worker_id)
	db.session.add(entry)
	db.session.commit()

@app.route('/events',  methods = ['GET', 'POST'])
#@login_required
def projects():
	columns = []
	columns.append(ColumnDT('id'))
	columns.append(ColumnDT('user_id'))
	columns.append(ColumnDT('timestamp'))
	columns.append(ColumnDT('project_id'))
	columns.append(ColumnDT('file_id'))
	columns.append(ColumnDT('job_id'))
	columns.append(ColumnDT('worker_id'))
	columns.append(ColumnDT('type'))
	query = db.session.query(Event)
	rowTable = DataTables(request, Event, query, columns)
	return jsonify(rowTable.output_result())
