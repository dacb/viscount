"""
viscount.users.forms

Note: these are handled by flask-security and exist just for the API
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from ..services import roles as _roles

__all__ = ['NewUserForm', 'UpdateUserForm']


class NewUserForm(Form):
	email = StringField('email', validators=[Required(), Email()])
	username = StringField('username', validators=[Required()])
	password = StringField('password', validators=[Required()])
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])
	roles = QuerySelectMultipleField('roles', query_factory=_roles.all)


class UpdateUserForm(Form):
	email = StringField('email', validators=[Required(), Email()])
	username = StringField('username', validators=[Required()])
	password = StringField('password', validators=[Required()])
	firstName = StringField('firstName', validators=[Required()])
	lastName = StringField('lastName', validators=[Required()])
	roles = QuerySelectMultipleField('roles', query_factory=_roles.all)
