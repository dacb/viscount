# -*- coding: utf-8 -*-
"""
viscount.file.forms

File related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional

from ..services import files

__all__ = ['NewFileForm', 'UpdateFileForm']


class NewFileForm(Form):
	 name = StringField('Name', validators=[Required()])
	 description = TextAreaField('Description', validators=[Required()])


class UpdateFileForm(Form):
	 name = StringField('Name', validators=[Optional()])
	 description = TextAreaField('Description', validators=[Optional()])

