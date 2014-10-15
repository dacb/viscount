from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db
from .event import Event

@app.route('/')
@app.route('/index')
@login_required
def index():
	my_events = db.session.query(Event).filter_by(user_id = g.user.id).order_by(Event.timestamp.desc()).limit(5).all()
	global_events = db.session.query(Event).order_by(Event.timestamp.desc()).limit(5).all()
	return render_template("index.html", title='Home', user=g.user, my_events=my_events, global_events=global_events)

@app.route("/robots.txt")
def robotsTxt():
	return send_from_directory(app.static_folder, "robots.txt")
