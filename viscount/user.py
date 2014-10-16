# authentication associated
# User data model
# LoginForm processor
# login and logout endpoints

from flask.ext.wtf import Form
from wtforms import form, fields, validators
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import Bcrypt
from datetime import datetime

from viscount import app
from viscount.database import db
from viscount.datatables import DataTables

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"

bcrypt = Bcrypt()

# fetch user info
@login_manager.user_loader
def user_loader(user_id):
	return db.session.query(User).filter_by(id=user_id).first()

# pre request setup
@app.before_request
def before_request():
	g.user = current_user

# models
class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), index=True, unique=True)
	firstName = db.Column(db.String(64))
	lastName = db.Column(db.String(64))
	email = db.Column(db.String(255), index=True, unique=True)
	password = db.Column(db.String(255))
	isActive = db.Column(db.Boolean(), default=True)
	created = db.Column(db.DateTime(), default=datetime.utcnow())
	last_login = db.Column(db.DateTime())
	current_login = db.Column(db.DateTime())
	last_login_ip = db.Column(db.String(15))
	current_login_ip = db.Column(db.String(15))
	login_count = db.Column(db.Integer, default=0)
	role = db.Column(db.Enum('admin', 'user', 'guest'))
	# setup relationships
	events = db.relationship('Event', backref='user', lazy='dynamic')
	files = db.relationship('File', backref='user', lazy='dynamic')
	jobs = db.relationship('Job', backref='user', lazy='dynamic')
	
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3

	def as_dict(self):
		return { c.name: getattr(self, c.name) for c in self.__table__.columns }

	def __repr__(self):
		return '<User %r>' % (self.username)

from .event import Event, eventEntry

def userCreate(username, password, role, lastName=None, firstName=None, email=None):
	user = User(username=username, lastName=lastName, firstName=firstName, password=bcrypt.generate_password_hash(password), email=email, role=role)
	db.session.add(user)
	eventEntry(user=user, type='created')
	return user

def modifyUser(user, username, password, role, lastName, firstName, email):
	user.username = username
	user.password = password
	user.lastName = lastName
	user.firstName = firstName
	user.email = email
	user.role = role
	eventEntry(user=user, type='modified')
	return user

class LoginForm(Form):
	username = fields.StringField('username', validators=[validators.required()])
	password = fields.PasswordField('username', validators=[validators.required()])
	remember_me = fields.BooleanField('remember_me', default=True)

# login form
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.query(User).filter_by(username = form.username.data).first()
		if user and user.isActive and bcrypt.check_password_hash(user.password, form.password.data):
			session['remember_me'] = form.remember_me.data
			user.authenticated = True
			user.current_login = datetime.utcnow()
			user.current_login_ip = request.remote_addr
			user.login_count += 1
			db.session.add(user)
			eventEntry(user=user, type='login')
			login_user(user, remember=form.remember_me.data)
			return redirect(url_for('index'))
		flash('Username or password invalid')
	return render_template("login.html", title='Login', form=form)

# logout form
@app.route('/logout')
@login_required
def logout():
	user = g.user
	user.authenticated = False
	user.last_login = user.current_login
	user.last_login_ip = user.current_login_ip
	db.session.add(user)
	eventEntry(user=user, type='logout')
	logout_user()
	flash('You have logged out')
	return redirect(url_for('login'))
