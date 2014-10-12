from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), index=True, unique=True)
	description = db.Column(db.Text, index=False, unique=False)

	def __repr__(self):
		return '<Project %r>' % (self.name)

@app.route('/projects')
@login_required
def projects():
	user = g.user
	projects = db.session.query(Project).all()
	return render_template('projects.html', user=user, projects=db.session.query(Project).all())

@app.route('/project/<id>')
@login_required
def project(id):
	user = g.user
	project = db.session.query(Project).filter_by(id = id).first()
	if project == None:
		flash('Project with ID %s not found.' % id)
		return redirect(url_for('projects'))
	return render_template('project.html', user=user, project=project)
