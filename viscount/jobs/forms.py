# -*- coding: utf-8 -*-
"""
viscount.job.forms

Job related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional

from ..services import jobs

__all__ = ['NewJobForm', 'UpdateJobForm']


class NewJobForm(Form):
	 name = StringField('Name', validators=[Required()])
	 description = TextAreaField('Description', validators=[Required()])


class UpdateJobForm(Form):
	 name = StringField('Name', validators=[Optional()])
	 description = TextAreaField('Description', validators=[Optional()])

