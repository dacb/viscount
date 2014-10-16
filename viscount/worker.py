from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required

from viscount import app
from viscount.database import db
from viscount.datatables import DataTables, ColumnDT, DataTables

class Worker(db.Model):
	__tablename__ = 'worker'

	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.Enum('idle', 'expired', 'active', 'failed'), index=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
	# setup relationships
	events = db.relationship('Event', backref='worker', lazy='dynamic')

	def __init__(self):
		from viscount.event import Event
		self.state = 'idle'
		db.session.add(Event('created', worker=self))

	def __repr__(self):
		return '<Worker %r>' % (self.name)

@app.route('/worker/<id>')
@login_required
def worker(id):
	worker = db.session.query(Worker).get(id)
	if file is None:
		flash('Worker with ID %s not found.' % id)
		return redirect(url_for('workers'))
	return render_template('worker.html', user=g.user, worker=worker)

@app.route('/workers')
@login_required
def workers():
	idle_workers = db.session.query(Worker).filter_by(state='idle').all()
	expired_workers = db.session.query(Worker).filter_by(state='expired').all()
	active_workers = db.session.query(Worker).filter_by(state='active').all()
	failed_workers = db.session.query(Worker).filter_by(state='failed').all()
	return render_template('workers.html', user=g.user, workers=workers)
