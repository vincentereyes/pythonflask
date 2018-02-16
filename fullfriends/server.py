from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'mydb')
@app.route('/')
def index():
	query = "SELECT name, age, date_format(friendsince, '%M %d %Y') as dates FROM friends"
	friends = mysql.query_db(query)
	# print friends
	return render_template('index.html', all_friends= friends)
@app.route('/addfriend', methods=['POST'])
def create():
    # add a friend to the database!
    query = "INSERT INTO friends (name, age, friendsince) VALUES (:sname, :sage, NOW())"
    data = {
    	'sname': request.form['iname'],
    	'sage': request.form['iage']
    }
    # query = "INSERT INTO friends (name, age, friends)"
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
