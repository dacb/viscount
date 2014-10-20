# -*- coding: utf-8 -*-
"""
viscount.worker.forms

Worker related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional

from ..services import workers

__all__ = ['NewWorkerForm', 'UpdateWorkerForm']


class NewWorkerForm(Form):
	 name = StringField('Name', validators=[Required()])
	 description = TextAreaField('Description', validators=[Required()])


class UpdateWorkerForm(Form):
	 name = StringField('Name', validators=[Optional()])
	 description = TextAreaField('Description', validators=[Optional()])

