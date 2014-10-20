# -*- coding: utf-8 -*-
"""
viscount.task.forms

Task related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional

from ..services import tasks

__all__ = ['NewTaskForm', 'UpdateTaskForm']


class NewTaskForm(Form):
	 name = StringField('Name', validators=[Required()])
	 description = TextAreaField('Description', validators=[Required()])


class UpdateTaskForm(Form):
	 name = StringField('Name', validators=[Optional()])
	 description = TextAreaField('Description', validators=[Optional()])

