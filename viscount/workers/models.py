# -*- coding: utf-8 -*-
"""
viscount.worker.models

Worker models
"""

from ..core import db
from ..utils import JSONSerializer


class WorkerJSONSerializer(JSONSerializer):
	pass


class Worker(WorkerJSONSerializer, db.Model):
	__tablename__ = 'workers'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.Text, index=False, unique=False)

	events = db.relationship('Event', backref='worker', lazy='dynamic')

	def __repr__(self):
		return '<Worker %r>' % (self.name)
