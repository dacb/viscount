# -*- coding: utf-8 -*-
"""
viscount.job.models

Job models
"""

from ..core import db
from ..utils import JSONSerializer


jobs_files = db.Table(
		'jobs_files',
		db.Column('job_id', db.Integer(), db.ForeignKey('jobs.id')),
		db.Column('file_id', db.Integer(), db.ForeignKey('files.id')),
		db.Column('type', db.Enum('input', 'output'), index=True, nullable=False)
	)

job_dependencies = db.Table(
		'job_dependencies',
		db.Column('job_id', db.Integer(), db.ForeignKey('jobs.id')),
		db.Column('depends_on_job_id', db.Integer(), db.ForeignKey('jobs.id'))
	)


class JobJSONSerializer(JSONSerializer):
	pass


class Job(JobJSONSerializer, db.Model):
	__tablename__ = 'jobs'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.Text, index=False, unique=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
	state = db.Column(db.Enum('queued', 'running', 'finished', 'failed'), index=True, nullable=False)
	command = db.Column(db.Text)

	events = db.relationship('Event', backref='job', lazy='dynamic')
#	files = db.relationship('File', secondary=jobs_files, backref=db.backref('jobs', lazy='joined'))
	depends_on_jobs = db.relationship('Job', secondary=job_dependencies, 
							primaryjoin=(job_dependencies.c.job_id == id),
							secondaryjoin=(job_dependencies.c.depends_on_job_id == id),
							backref=db.backref('depends_on_me', lazy='dynamic'),
							lazy='dynamic'
						)

	def __repr__(self):
		return '<Job %r>' % (self.name)
