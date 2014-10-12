from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(255), index=True, unique=False)
	description = db.Column(db.Text, index=False, unique=False)
	md5sum = db.Column(db.String(32), index=True, unique=True)
	# setup relationships
	log_entries = db.relationship('Log', backref='file', lazy='dynamic')

	def __repr__(self):
		return '<File %r>' % (self.name)
