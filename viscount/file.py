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
	logEntry(user=user, file=file, type='created')
	return file

@app.route('/file/<id>')
@login_required
def fileSend(id):
	file = db.session.query(File).get(id)
	if file is None:
		flash('File with ID %s not found.' % id)
		return redirect(url_for('files'))
	return send_from_directory(app.config['UPLOADED_FILES_DEST'], file.filename)

@app.route('/files')
@login_required
def files():
	files = db.session.query(File).all()
	return render_template('files.html', user=g.user, files=files);

@app.route('/upload', methods=['POST'])
@login_required
def upload():
	file = request.files['file']
	if file is not None and fileAllowed(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOADED_FILES_DEST'], filename))
		return redirect(url_for('files'))
