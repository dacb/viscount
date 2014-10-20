"""
viscount.users.forms

Note: these are handled by flask-security and exist just for the API
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional

from ..services import users

__all__ = ['NewUserForm', 'UpdateUserForm']


class NewUserForm(Form):
	username = StringField('username', validators=[Required()])
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])


class UpdateUserForm(Form):
	username = StringField('username', validators=[Optional()])
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])

