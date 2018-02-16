from flask import Flask, request, redirect, render_template, flash, session
from mysqlconnection import MySQLConnector
import re
import md5

name_regex = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'motorsport'
mysql = MySQLConnector(app,'mydb')

@app.route('/')
def index():
    if 'id' not in session:
        session['id'] = 0
    else:
        session['id'] = 0
        
    return render_template('index.html')

@app.route('/reg', methods=['POST'])
def lego():
    count = 0;
    if len(request.form['email']) < 1 or len(request.form['fname']) < 2 or len(request.form['lname']) < 2 or len(request.form['pword']) < 1 or len(request.form['cpword']) < 1:
        flash('Dont leave a field blank or inputs are too short!')
    else: 
        count += 1
    if not name_regex.match(request.form['fname']) and not name_regex.match(request.form['fname']):
        flash('Letters only for names please')
    else:
        count += 1
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address!')
    else:
        count += 1
    if len(request.form['pword']) < 9:
        flash('Password should be more than 8 characters')
    else:
        count += 1
    if not request.form['pword'] == request.form['cpword']:
        flash('Passwords do not match')
    else:
        count +=1

    query = 'SELECT * FROM uzer where email = :semail'
    data = {'semail': request.form['email']}
    emails = mysql.query_db(query, data)
    print emails
    if len(emails) > 0:
        flash("Email already exists")
    else:
        count +=1

    if count == 6:
        query = 'INSERT INTO uzer (fname, lname, email, password) VALUES (:sfname, :slname, :semail, :spw)'
        data = {
            'sfname': request.form['fname'],
            'slname': request.form['lname'],
            'semail': request.form['email'],
            'spw': md5.new(request.form['pword']).hexdigest()
            }
        mysql.query_db(query, data)
        flash('Thanks for submitting your application')
        data2 = {'boom': request.form['email']}
        query2 = 'SELECT id FROM uzer WHERE email = :boom'
        ideez = mysql.query_db(query2, data2)
        session['id'] = ideez[len(ideez)-1]['id']
        return redirect('/success')
    else:
        return redirect('/')

@app.route('/log', methods=['POST'])
def eskitiit():
    password = md5.new(request.form['pword1']).hexdigest()
    email = request.form['email1']
    user_query = "SELECT * FROM uzer where uzer.email = :email AND uzer.password = :password"
    query_data = { 'email': email, 'password': password}
    user = mysql.query_db(user_query, query_data)

    data2 = {'boom': request.form['email1']}
    query2 = 'SELECT id FROM uzer WHERE email = :boom'
    ideez = mysql.query_db(query2, data2)
    session['id'] = ideez[len(ideez)-1]['id']

    if len(user) > 0:
        return redirect('/success')
    else:
        flash("Invalid Credentials")
        return redirect('/')


@app.route('/success')
def yo():
    query = "SELECT fname, lname from uzer where id = :idee"
    data = {'idee': session['id']}
    info = mysql.query_db(query, data)
    print session['id'], info
    return render_template('success.html', info=info)

app.run(debug=True)
