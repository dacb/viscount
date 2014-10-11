from viscount.server import db

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), index=True, unique=True)
	description = db.Column(db.Text, index=False, unique=False)

	def __repr__(self):
		return '<Project %r>' % (self.name)

class ChangeLog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	type = db.Column(db.Enum('created', 'modified'))
	message = db.Column(db.Text, index=False, unique=False)

	def __repr__(self):
		return '<ChangeLog %r>' % (self.id)

