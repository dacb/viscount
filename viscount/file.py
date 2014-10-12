from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from flask.ext.login import login_required
from .server import app, db

class File(db.Model):
	__tablename__ = 'file'

	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(255), index=True, unique=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	description = db.Column(db.Text, index=False, unique=False)
	md5sum = db.Column(db.String(32), index=True, unique=True)
	# setup relationships
	log_entries = db.relationship('Log', backref='file', lazy='dynamic')
#	input_file = db.relationship('Job', backref='input_file', lazy='dynamic')
#	output_file = db.relationship('Job', backref='output_file', lazy='dynamic')

	def __repr__(self):
		return '<File %r>' % (self.name)

def fileCreate(filename, description, md5sum, user):
	file = File(filename=filename, description=description, md5sum=md5sum, user_id=user.id)
        db.session.add(file)
        db.session.commit()
        logEntry(user=user, file=project, type='created')
	return file

@app.route('/file/<id>')
def fileSend(id):
	file = db.session.query(Files).get(id)
	return send_from_directory(app.config['FILE_DIR'], file.filename)
