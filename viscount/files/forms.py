# -*- coding: utf-8 -*-
"""
viscount.file.forms

File related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import Required, Optional

from ..services import files

__all__ = ['NewFileForm', 'UpdateFileForm']


class NewFileForm(Form):
	name = StringField('Name', validators=[Required()])
	description = TextAreaField('Description', validators=[Required()])


class UpdateFileForm(Form):
	description = TextAreaField('Description', validators=[Optional()])

