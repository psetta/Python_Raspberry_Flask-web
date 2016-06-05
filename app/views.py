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
		user_name = flask.session["key"][0]
		user_perm = flask.session["key"][1]
		return flask.render_template("index.html",
				style="#mensaje {text-align: center;}",
				user = user_name)
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
	####PROBAS####
	if flask.request.form["user"] == "test":
		flask.session["key"] = ["test","",""]
		return flask.redirect('/')
	##############
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
		else:
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
		ssh_table = open(app.static_folder+"/sshlog.log","r").read().decode("utf-8")
		ssh_table = ssh_table.split("\n")
		estilo_ssh = open(app.static_folder+"/style/sshlog.css","r").read().decode("utf-8")
		user_name = flask.session["key"][0]
		return flask.render_template("sshlog.html",
				style = estilo_ssh,
				sshlog = ssh_table,
				user = user_name)
	else:
		return flask.redirect('/')
		
@app.route('/terminal')
def terminal():
	if "key" in flask.session:
		user_name = flask.session["key"][0]
		return flask.render_template("terminal.html",
				style="#terminal {text-align: center;}",
				user = user_name)
	else:
		return flask.redirect('/')
		
@app.route('/_command')
def command():
	if "key" in flask.session:
		comando = flask.request.args.get('comando')
		salida = comando
		try:
			salida = os.popen(comando).read()
		except:
			salida = "Error"
		return flask.jsonify(result=unicode(salida,errors='ignore'))
	else:
		return flask.redirect('/')
