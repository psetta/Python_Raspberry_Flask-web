# -*- coding: utf-8 -*-

from app import app
import os
import flask

app.secret_key = os.urandom(24)
 
@app.route('/')
@app.route('/index')
def index():
	if "key" in flask.session:
		return flask.render_template("index.html",
				style="#mensaje {text-align: center;}")
	else:
		return flask.redirect("/login")

@app.route('/login')
def login():
	if False:
		return flask.redirect("/index")
	else:
		return flask.render_template("login.html",
				style="#login {text-align: center;}")

@app.route('/signup', methods = ['POST'])				
def signup():
	passwd = flask.request.form["passwd"]
	if passwd == "rodaballo":
		flask.session["key"] = os.urandom(24)
	return flask.redirect('/')

@app.route('/logout')
def logout():
    flask.session.pop("key", None)
    return flask.redirect("/")