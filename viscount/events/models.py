# -*- coding: utf-8 -*-
"""
viscount.event.models

Event models
"""

from datetime import datetime

from ..core import db
from ..utils import JSONSerializer


class EventJSONSerializer(JSONSerializer):
	pass


class Event(EventJSONSerializer, db.Model):
	__tablename__ = 'events'	

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow())
	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
	file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
	workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))
	task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
	job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
	worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'))
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
				msg.append('user %s' % self.user.name)
		if self.type is not None:
				msg.append(self.type)
		if self.project is not None:
				msg.append('project %s' % self.project.name)
		if self.file is not None:
				msg.append('file %s' % self.file.filename)
		return ' : '.join(msg)

