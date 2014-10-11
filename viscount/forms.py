from flask.ext.wtf import Form
from wtforms import form, fields, validators

class LoginForm(Form):
	username = fields.StringField('username', validators=[validators.required()])
	password = fields.PasswordField('username', validators=[validators.required()])
	remember_me = fields.BooleanField('remember_me', default=False)
