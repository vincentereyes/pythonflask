from flask import Flask, request, redirect, render_template, flash, session
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'motorsport'
mysql = MySQLConnector(app,'friendsdb')

@app.route('/users')
def index():
	query = "SELECT id, CONCAT(first_name, ' ', last_name) as name, email, date_format(created_at, '%M %d %Y' ) as dates from friends"
	data = mysql.query_db(query)
	return render_template('index.html', all_friends=data)

@app.route('/users/new')
def rendernewuser():
	return render_template('newuser.html')

@app.route('/users/<uid>/edit')
def renderedit(uid):
	query = "SELECT id, first_name, last_name, email from friends where id = " + uid
	data = mysql.query_db(query)
	return render_template('edituser.html', friend=data)

@app.route('/users/<uid>', methods=['POST'])
def updateinfo(uid):
	query = "UPDATE friends SET first_name = :fname, last_name = :lname, email = :email WHERE id = " + uid
	data = {
		'fname': request.form['fname'],
		'lname': request.form['lname'],
		'email': request.form['email2']
		}
	mysql.query_db(query, data)

	return redirect('/users/' + uid + '')

@app.route('/users/<uid>')
def show(uid):
	query = "SELECT id, CONCAT(first_name, ' ', last_name) as name, email, date_format(created_at, '%M %d %Y' ) as frienddate from friends where id = " + uid
	data = mysql.query_db(query)
	print data

	return render_template('show.html', friend=data)

@app.route('/users/create', methods=['POST'])
def insertion():
	query = 'INSERT INTO friends (first_name, last_name, email) VALUES (:fname, :lname, :email)'
	data = {
		'email': request.form['email'],
		'fname': request.form['fname'],
		'lname': request.form['lname']
		}

	mysql.query_db(query, data)
	query = "SELECT id from friends"
	data = mysql.query_db(query)
	idee = str(data[len(data)-1]['id'])
	
	return redirect('/users/' + idee)

@app.route('/users/<uid>/destroy')
def delete(uid):
	query = "DELETE FROM friends where id = " + uid
	mysql.query_db(query)
	return redirect('/users')

app.run(debug=True)







