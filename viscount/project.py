from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db
from .log import logEntry

class Project(db.Model):
	__tablename__ = 'project'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), index=True, unique=True)
	description = db.Column(db.Text, index=False, unique=False)
        # setup relationships
        log_entries = db.relationship('Log', backref='project', lazy='dynamic')
        jobs = db.relationship('Job', backref='project', lazy='dynamic')

	def __repr__(self):
		return '<Project %r>' % (self.name)

def projectCreate(name, description, user):
	project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()
        logEntry(user=user, project=project, type='created')
	return project

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
        logEntry(user=user, project=project, type='accessed')
	return render_template('project.html', user=user, project=project)
