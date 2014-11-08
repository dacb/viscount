# -*- coding: utf-8 -*-
"""
viscount.task.forms

Task related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, FieldList, FormField
from wtforms.validators import Required, Optional

from ..services import tasks

__all__ = ['NewTaskInputForm', 'NewTaskForm', 'UpdateTaskForm']


class NewTaskInputForm(Form):
	input_file_name = StringField('Input file name', validators=[Required()])
	input_file_description = TextAreaField('Input file description', validators=[Required()])
	intut_file_type_id = IntegerField('Input file type', validators=[Required()])


class NewTaskForm(Form):
	name = StringField('Name', validators=[Required()])
	description = TextAreaField('Description', validators=[Required()])
	source = IntegerField('Source', validators=[Required()])
	inputs = FieldList(FormField(NewTaskInputForm))


class UpdateTaskForm(Form):
	name = StringField('Name', validators=[Optional()])
	description = TextAreaField('Description', validators=[Optional()])

