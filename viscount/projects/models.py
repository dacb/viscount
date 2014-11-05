# -*- coding: utf-8 -*-
"""
viscount.project.models

Project models
"""

from ..core import db
from ..utils import JSONSerializer


projects_workflows = db.Table(
	'projects_workflows',
	db.Column('project_id', db.Integer(), db.ForeignKey('projects.id')),
	db.Column('workflow_id', db.Integer(), db.ForeignKey('workflows.id')))


class ProjectJSONSerializer(JSONSerializer):
	pass


class Project(ProjectJSONSerializer, db.Model):
	__tablename__ = 'projects'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	description = db.Column(db.Text, index=False, unique=False)

	events = db.relationship('Event', backref='project', lazy='dynamic')
	workflows = db.relationship('Workflow', secondary=projects_workflows, backref=db.backref('projects', lazy='dynamic'))

	def __repr__(self):
		return '<Project %r>' % (self.name)
