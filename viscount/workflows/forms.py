# -*- coding: utf-8 -*-
"""
viscount.workflow.forms

Workflow related forms
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional

from ..services import workflows

__all__ = ['NewWorkflowForm', 'UpdateWorkflowForm']


class NewWorkflowForm(Form):
	 name = StringField('Name', validators=[Required()])
	 description = TextAreaField('Description', validators=[Required()])


class UpdateWorkflowForm(Form):
	 name = StringField('Name', validators=[Optional()])
	 description = TextAreaField('Description', validators=[Optional()])

