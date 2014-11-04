# -*- coding: utf-8 -*-
"""
viscount.file.models

File models
"""

from ..core import db
from ..utils import JSONSerializer


class FileJSONSerializer(JSONSerializer):
	__json_hidden__ = ['file']
	__json_modifiers__ = {
		'events': lambda events, _: [dict(id=event.id) for event in events],
	}


class File(FileJSONSerializer, db.Model):
	__tablename__ = 'files'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), index=False, unique=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	description = db.Column(db.Text, index=False, unique=False)
	md5sum = db.Column(db.String(32), index=True, unique=False)
	file = db.Column(db.Text, index=False, unique=False)

	events = db.relationship('Event', backref='file', lazy='dynamic')

	def __repr__(self):
		return '<File %r>' % (self.name)
