from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_required
from .server import app, db

@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template("index.html", title='Home', user=g.user)

@app.route("/robots.txt")
def robotsTxt():
        return send_from_directory(app.static_folder, "robots.txt")

