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

app.run(debug=True)