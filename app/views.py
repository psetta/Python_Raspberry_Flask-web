# -*- coding: utf-8 -*-

from app import app
import flask
import os
import re
import MySQLdb

app.secret_key = os.urandom(24)
 
@app.route('/')
@app.route('/index')
def index():
	if "key" in flask.session:
		nombre = flask.session["key"][0]
		permisos = flask.session["key"][1]
		return flask.render_template("index.html",
				style="#mensaje {text-align: center;}",
				user = nombre)
	else:
		return flask.redirect("/login")

@app.route('/login')
def login():
	if "key" in flask.session:
		return flask.redirect("/")
	else:
		return flask.render_template("login.html")

@app.route('/signup', methods = ['POST'])				
def signup():
	if "key" in flask.session:
		return flask.redirect("/")
	else:
		db = False
		try:
			db = MySQLdb.connect("localhost","root","1234","psettamaxima_db" )
		except:
			None
		if db:
			cursor = db.cursor()
			user = flask.request.form["user"]
			passwd = flask.request.form["passwd"]
			user = user.strip()
			passwd = passwd.strip()
			if re.findall(""'"|'"'",user) or re.findall(""'"|'"'",passwd):
				return flask.redirect('/')
			try:
				consulta = ("select name,perm from users where name = '"+user+
								"' and  pass = '"+passwd+"';")
				cursor.execute(consulta)
				data = cursor.fetchone()
				db.close()
				if data:
					flask.session["key"] = data
					return flask.redirect('/')
				else:
					return flask.redirect('/')
			except:
				db.close()
				return flask.redirect("/login")

@app.route('/logout')
def logout():
	if "key" in flask.session:
		flask.session.pop("key", None)
		return flask.redirect("/")
	else:
		return flask.redirect('/')

@app.route('/sshlog')
def sshlog():
	if "key" in flask.session:
		ssh = open(app.static_folder+"/sshlog.log","r").read().decode("utf-8")
		ssh = ssh.split("\n")
		return flask.render_template("sshlog.html",
				style="""
				#sshlog table {font-size: 90%;}
				#sshlog table {margin: 0 auto; border: 0.2em solid #C3F5D6; padding: 0.5em;}
				#sshlog table th {border: 0.2em solid lightgray; background-color: #F0F0F0; margin: 1em; padding: 0.2em;}
				#sshlog table td {border: 0.2em solid #F0F0F0; padding: 0.2em; margin: 0.5em;  max-width: 25em;
						min-width: 3em; overflow: hidden; text-overflow: ellipsis;}
				#sshlog table tr:hover {background-color: #F0F0F0;}
				#sshlog table td:hover {background-color: #C3F5D6; overflow: visible;}
				""",
				sshlog=ssh)
	else:
		return flask.redirect('/')