from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db

class Worker(db.Model):
	__tablename__ = 'worker'

	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.Enum('idle', 'expired', 'active', 'failed'), index=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
	# setup relationships
	log_entries = db.relationship('Event', backref='worker', lazy='dynamic')

	def __repr__(self):
		return '<Worker %r>' % (self.name)

def workerCreate():
	worker = Worker(state='idle')
        db.session.add(worker)
        db.session.commit()
        eventEntry(worker=worker, type='created')
	return file

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
