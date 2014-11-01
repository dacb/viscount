"""
viscount.users.forms

Note: these are handled by flask-security and exist just for the API
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import Required, Email

from ..services import users

__all__ = ['NewUserForm', 'UpdateUserForm']


class NewUserForm(Form):
	email = StringField('email', validators=[Required(), Email()])
	username = StringField('username', validators=[Required()])
	password = StringField('password', validators=[Required()])
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])
	roles = SelectMultipleField('roles', choices=[('admin', '1'), ('user', '2'), ('guest', '3')])


class UpdateUserForm(Form):
	email = StringField('email', validators=[Required(), Email()])
	username = StringField('username', validators=[Required()])
	password = StringField('password', validators=[Required()])
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])

