from flask import Flask, request, redirect, render_template, flash, session
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'motorsport'
mysql = MySQLConnector(app,'mydb')
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/checkemail', methods=['POST'])
def create():
    # add a friend to the database!
    query = 'SELECT * FROM emails where email = :semail'
    query2 = 'INSERT INTO emails (email, created_at) VALUES (:semail, NOW())'
    data = {
    	'semail': request.form['iemail'],
    }
    # query = "INSERT INTO friends (name, age, friends)"
    emails = mysql.query_db(query, data)
    # session['mail'] = emails[0]
    if len(emails) > 0:
        flash("INVALID EMAIL")
        return redirect("/")
    else:
        mysql.query_db(query2, data)
        return redirect('/success')

@app.route('/success')
def yo():
    query3 = "SELECT * FROM emails"
    all_emails = mysql.query_db(query3)
    flash("The email address you entered: "+ all_emails[len(all_emails)-1]['email'] + " is a VALID email address Thanks ")

    return render_template('success.html', all_emails=all_emails)

app.run(debug=True)
