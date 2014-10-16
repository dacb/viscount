import os
from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from flask.ext.login import login_required
from werkzeug import secure_filename

from viscount import app
from viscount.database import db
from viscount.datatables import DataTables, ColumnDT, DataTables

class File(db.Model):
	__tablename__ = 'file'

	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(255), index=False, unique=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	description = db.Column(db.Text, index=False, unique=False)
	md5sum = db.Column(db.String(32), index=True, unique=False)
	# setup relationships
	events = db.relationship('Event', backref='file', lazy='dynamic')

	def __init__(self, filename, user_id, description):
		from viscount.event import Event
		self.filename = filename
		self.user_id = user.id
		self.description = description
		db.session.add(Event('created', file=self))

	def __repr__(self):
		return '<File %r>' % (self.name)

@app.route('/files')
@login_required
def files():
	files = db.session.query(File).all()
	return render_template('files.html', user=g.user, files=files);

@app.route('/file/<id>/<action>')
@login_required
def fileAction(id, action):
	file = db.session.query(File).get(id)
	if file is None:
		flash('File with ID %s not found.' % id)
		return redirect(url_for('files'))
	elif action == 'edit':
		return render_template('file.html', user=g.user, file=file);
	elif action == 'delete':
		if g.user.role != 'admin':
			flash('Only an admin can delete a file!')
			return redirect(url_for('files'))
		flash('File deleting is not currently supported.')
		return redirect(url_for('files'))
	return send_from_directory(os.path.join(app.config['UPLOAD_DEST'], str(file.id)), file.filename, as_attachment=True, attachment_filename=file.filename)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
@login_required
def upload():
	file = request.files['file']
	print file
	if file:
		# check the file type based on extension
		if allowed_file(file.filename):
			# cleanup the filename
			filename = secure_filename(file.filename)
			# create the file record
			frec = fileCreate(filename=filename, user=g.user)
			# save the file
			savedir = os.path.join(app.config['UPLOAD_DEST'], str(frec.id))
			os.makedirs(savedir)
			savepath = os.path.join(savedir, filename)
			file.save(savepath)
			flash('File %s has been uploaded successfully.' % file.filename)
		else:
			flash('File type %s is not on the white list!' % file.filename.rsplit('.', 1)[1])
	else:
		flash('File upload failed!')
	return redirect(url_for('files'));
