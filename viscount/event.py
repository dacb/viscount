import datetime
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_required

from viscount import app
from viscount.database import db
from viscount.datatables import DataTables, ColumnDT, DataTables

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

@app.route('/events',  methods = ['GET', 'POST'])
#@login_required
def events():
	columns = []
	columns.append(ColumnDT('id'))
	columns.append(ColumnDT('user_id'))
	columns.append(ColumnDT('user.username'))
	columns.append(ColumnDT('timestamp'))
	columns.append(ColumnDT('project_id'))
	columns.append(ColumnDT('file_id'))
	columns.append(ColumnDT('job_id'))
	columns.append(ColumnDT('worker_id'))
	columns.append(ColumnDT('type'))
	query = db.session.query(Event).outerjoin(User, (User.id == Event.user_id))
	rowTable = DataTables(request, Event, query, columns)
	return jsonify(rowTable.output_result())
