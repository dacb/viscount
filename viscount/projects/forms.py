"""
viscount.project.forms

Project related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional

from ..services import projects

__all__ = ['NewProjectForm', 'UpdateProjectForm']


class NewProjectForm(Form):
	name = StringField('Name', validators=[Required()])
	description = TextAreaField('Description', validators=[Required()])

class UpdateProjectForm(Form):
	name = StringField('Name', validators=[Optional()])
	description = TextAreaField('Description', validators=[Optional()])

