from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db
from .file import File
from .event import eventEntry

class JobFiles(db.Model):
	__tablename__ = 'job_files'

	job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False, primary_key=True)
	file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False, primary_key=True)
	type = db.Column(db.Enum('input', 'output'), index=True)

class Job(db.Model):
	__tablename__ = 'job'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
	state = db.Column(db.Enum('queued', 'running', 'finished', 'failed'), index=True, nullable=False)
	command = db.Column(db.Text)
	# setup relationships
	events = db.relationship('Event', backref='job', lazy='dynamic')
	files = db.relationship('JobFiles', backref='job', lazy='dynamic')

	def __repr__(self):
		return '<Job %r>' % (self.id)

def jobCreate(user, project, command, input_files=[]):
	job = Job(user_id=user.id, project_id=project.id, command=command, files=input_files, state='queued')
        db.session.add(job)
        eventEntry(user=user, project=project, job=job, type='created')
	return file

@app.route('/job/<id>')
@login_required
def job(id):
	job = db.session.query(Job).get(id)
	if file is None:
		flash('Job with ID %s not found.' % id)
		return redirect(url_for('jobs'))
	return render_template('job.html', user=g.user, job=job)

@app.route('/jobs')
@login_required
def jobs():
	queued_jobs = db.session.query(Job).filter_by(state='queued').all()
	running_jobs = db.session.query(Job).filter_by(state='running').all()
	finished_jobs = db.session.query(Job).filter_by(state='finished').all()
	failed_jobs = db.session.query(Job).filter_by(state='failed').all()
	return render_template('jobs.html', user=g.user, queued_jobs=queued_jobs, running_jobs=running_jobs, finished_jobs=finished_jobs, failed_jobs=failed_jobs)
