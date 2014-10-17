import decimal
import datetime

from flask.ext.sqlalchemy import SQLAlchemy

from viscount import app

db = SQLAlchemy(app)

def init_user(username, password, role):
	from viscount.user import User
	from viscount.event import Event
	user = User(username=username, password=password, role=role)
	db.session.add(user)
	db.session.add(Event(type='created', user=user))
	return user

def init_project(name, description, user):
	from viscount.project import Project
	from viscount.event import Event
	project = Project(name=name, description=description)
	db.session.add(project)
	db.session.add(Event(type='created', project=project, user=user))
	return project

def init_defaults():
	from viscount.event import Event
	db.session.add(Event(type='created'))
	init_user(username='admin', password='admin', role='admin')
	init_user(username='user', password='user', role='user')
	init_user(username='guest', password='guest', role='guest')
	db.session.commit()

def init_samples():
	from viscount.user import User
	admin = db.session.query(User).get(1)
	for i in range(16):
		init_project(name='sample' + str(i), description='sample project ' + str(i), user=admin)
	db.session.commit()

def printquery(statement, bind=None):
	"""
	print a query, with values filled in
	for debugging purposes *only*
	for security, you should always separate queries from their values
	please also note that this function is quite slow
	"""
	import sqlalchemy.orm
	if isinstance(statement, sqlalchemy.orm.Query):
		if bind is None:
			bind = statement.session.get_bind(
					statement._mapper_zero_or_none()
			)
		statement = statement.statement
	elif bind is None:
		bind = statement.bind 

	dialect = bind.dialect
	compiler = statement._compiler(dialect)
	class LiteralCompiler(compiler.__class__):
		def visit_bindparam(
				self, bindparam, within_columns_clause=False, 
				literal_binds=False, **kwargs
		):
			return super(LiteralCompiler, self).render_literal_bindparam(
					bindparam, within_columns_clause=within_columns_clause,
					literal_binds=literal_binds, **kwargs
			)
		def render_literal_value(self, value, type_):
			"""Render the value of a bind parameter as a quoted literal.

			This is used for statement sections that do not accept bind paramters
			on the target driver/database.

			This should be implemented by subclasses using the quoting services
			of the DBAPI.

			"""
			if isinstance(value, basestring):
				value = value.replace("'", "''")
				return "'%s'" % value
			elif value is None:
				return "NULL"
			elif isinstance(value, (float, int, long)):
				return repr(value)
			elif isinstance(value, decimal.Decimal):
				return str(value)
			elif isinstance(value, datetime.datetime):
				return "TO_DATE('%s','YYYY-MM-DD HH24:MI:SS')" % value.strftime("%Y-%m-%d %H:%M:%S")

			else:
				raise NotImplementedError(
							"Don't know how to literal-quote value %r" % value)			

	compiler = LiteralCompiler(dialect, statement)
	print compiler.process(statement)
