from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db
from .log import Log

@app.route('/')
@app.route('/index')
@login_required
def index():
	my_log = db.session.query(Log).filter_by(user_id = g.user.id).order_by(Log.timestamp.desc()).limit(5).all()
	global_log = db.session.query(Log).order_by(Log.timestamp.desc()).limit(5).all()
	return render_template("index.html", title='Home', user=g.user, my_log=my_log, global_log=global_log)

@app.route("/robots.txt")
def robotsTxt():
	return send_from_directory(app.static_folder, "robots.txt")

def register_api(view, endpoint, url, pk='id', pk_type='int'):
	view_func = view.as_view(endpoint)
	app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET',])
	app.add_url_rule(url, view_func=view_func, methods=['POST',])
	app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])
