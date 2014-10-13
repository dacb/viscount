# authentication associated
# User data model
# LoginForm processor
# login and logout endpoints

from flask.ext.wtf import Form
from wtforms import form, fields, validators
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import Bcrypt
from flask.views import MethodView
import datetime
from .server import app, db

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
	created = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
	last_login = db.Column(db.DateTime())
	current_login = db.Column(db.DateTime())
	last_login_ip = db.Column(db.String(15))
	current_login_ip = db.Column(db.String(15))
	login_count = db.Column(db.Integer, default=0)
	role = db.Column(db.Enum('admin', 'user', 'guest'))
	# setup relationships
	log_entries = db.relationship('Log', backref='user', lazy='dynamic')
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

	def __repr__(self):
		return '<User %r>' % (self.username)

from .log import Log, logEntry

def userCreate(username, password, role, lastName=None, firstName=None, email=None):
	user = User(username=username, lastName=lastName, firstName=firstName, password=bcrypt.generate_password_hash(password), email=email, role=role)
	db.session.add(user)
	db.session.commit()
	logEntry(user=user, type='created')
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
			user.current_login = datetime.datetime.utcnow()
			user.current_login_ip = request.remote_addr
			user.login_count += 1
			db.session.add(user)
			db.session.commit()
			logEntry(user=user, type='login')
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
	db.session.commit()
	logEntry(user=user, type='logout')
	logout_user()
	flash('You have logged out')
	return redirect(url_for('login'))



class UserAPI(MethodView):
	decorators = [login_required]

	def get(self, user_id):
		if user_id is None:
			# return a list of users
			users = db.session.query(User).all()
			return render_template("users.html", title='Users', user=g.user, users=users)
		else:
			# expose a single user
			user = db.session.query(User).get(user_id)
			return render_template("user.html", title='User', user=g.user, user_target=user)

	def post(self):
		if g.user.role != 'admin':
			flash('You must be in the admin role to create a user.')
			return redirect(url_for('users'))
		else:
			flash('Created a user "test" with password "test".')
			# create a new user
			# WARNING: testing stub only
			new = createUser(username='test', password='test', role='user')
			# redirect to the user view page
			return redirect(url_for('user_api', user_id=new.id))

	def delete(self, user_id):
		# delete a single user
		if g.user.role != 'admin':
			flash('You must be in the admin role to delete a user.')
			return redirect(url_for('users'))
		else:
			if g.user.id == user_id:
				flash('You cannot delete yourself!')
			user = db.session.query(User).get(user_id)
			if user is not None:
				user.isActive = False
				db.session.commit()
			else:
				flash('User %d does not exist!' % user_id)
			return redirect(url_for('users'))
		pass

	def put(self, user_id):
		# update a single user
		flash('Not supported!')
		return redirect(url_for('users'))

from .views import register_api
register_api(UserAPI, 'user_api', '/users/', pk='user_id')
