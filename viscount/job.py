from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db

class Job(db.Model):
	__tablename__ = 'job'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
	state = db.Column(db.Enum('queued', 'running', 'finished', 'failed'))
	command = db.Column(db.Text)
	input_file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
	output_file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
	input_file = db.relationship('File', foreign_keys='Job.input_file_id')
	output_file = db.relationship('File', foreign_keys='Job.output_file_id')
	# setup relationships
	log_entries = db.relationship('Log', backref='job', lazy='dynamic')

	def __repr__(self):
		return '<File %r>' % (self.name)

def fileCreate(filename, description, md5sum, user):
	file = File(filename=filename, description=description, md5sum=md5sum, user_id=user.id)
        db.session.add(file)
        db.session.commit()
        logEntry(user=user, file=project, type='created')
	return file
