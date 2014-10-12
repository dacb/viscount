from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db

class Job(db.Model):
	__tablename__ = 'job'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
	state = db.Column(db.Enum('queued', 'running', 'finished', 'failed'), index=True)
	command = db.Column(db.Text)
	input_file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
	output_file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
	input_file = db.relationship('File', foreign_keys='Job.input_file_id')
	output_file = db.relationship('File', foreign_keys='Job.output_file_id')
	# setup relationships
	log_entries = db.relationship('Log', backref='job', lazy='dynamic')

	def __repr__(self):
		return '<Job %r>' % (self.name)

def jobCreate(user, project, command, input_file):
	job = Job(user_id=user.id, project_id=project.id, command=command, input_file_id=input_file.id)
        db.session.add(job)
        db.session.commit()
        logEntry(user=user, project=project, job=job, type='created')
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
	return render_template('jobs.html', user=g.user, jobs=jobs)
