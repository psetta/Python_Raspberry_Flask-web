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
	if "key" in flask.session:
		return flask.redirect("/")
	else:
		return flask.render_template("login.html",
				style="#login {text-align: center;}")

@app.route('/signup', methods = ['POST'])				
def signup():
	if "key" in flask.session:
		return flask.redirect("/")
	else:
		passwd = flask.request.form["passwd"]
		if passwd == "abrete":
			flask.session["key"] = os.urandom(24)
		return flask.redirect('/')

@app.route('/logout')
def logout():
	if "key" in flask.session:
		flask.session.pop("key", None)
		return flask.redirect("/")
	else:
		return flask.redirect('/')

#@app.route('/sshlog')
#def sshlog():
#	if "key" in flask.session:
#		ssh = open("static/sshlog.txt","r").readlines()
#		return flask.render_template("sshlog.html",
#				style="#sshlog {text-align: center; margin: 0 auto;}",
#				sshlog=ssh)
#	else:
#		return flask.redirect('/')