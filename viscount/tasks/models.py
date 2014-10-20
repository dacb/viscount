"""
viscount.task.models

Task models
"""

from ..core import db
from ..utils import JSONSerializer


class TaskJSONSerializer(JSONSerializer):
	__json_modifiers__ = {
		'events': lambda events, _: [dict(id=event.id) for event in events],
	}



class Task(TaskJSONSerializer, db.Model):
	__tablename__ = 'tasks'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	description = db.Column(db.Text, index=False, unique=False)

	events = db.relationship('Event', backref='task', lazy='dynamic')

	def __repr__(self):
		return '<Task %r>' % (self.name)
