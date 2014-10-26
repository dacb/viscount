"""
viscount.users.forms

Note: these are handled by flask-security and exist just for the API
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Optional, Email, AnyOf

from ..services import users

__all__ = ['NewUserForm', 'UpdateUserForm']


class NewUserForm(Form):
	email = StringField('email', validators=[Required(), Email()])
	username = StringField('username', validators=[Required()])
	password = StringField('password', validators=[Required()])
	roles = [StringField('role', validators=[Required(), AnyOf(values=['admin', 'user', 'guest'])])]
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])


class UpdateUserForm(Form):
	email = StringField('email', validators=[Required(), Email()])
	username = StringField('username', validators=[Required()])
	password = StringField('password', validators=[Required()])
	roles = [StringField('role', validators=[Required(), AnyOf(values=['admin', 'user', 'guest'])])]
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])

