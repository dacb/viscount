from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db

class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	type = db.Column(db.Enum('created', 'modified'))
	message = db.Column(db.Text, index=False, unique=False)

	def __repr__(self):
		return '<Log %r>' % (self.id)
