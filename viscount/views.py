from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db
from .logging import Log

@app.route('/')
@app.route('/index')
@login_required
def index():
	my_log = db.session.query(Log).filter_by(user_id = g.user.id).limit(5).all()
	global_log = db.session.query(Log).limit(5).all()
	return render_template("index.html", title='Home', user=g.user, my_log=my_log, global_log=global_log)

@app.route("/robots.txt")
def robotsTxt():
        return send_from_directory(app.static_folder, "robots.txt")

