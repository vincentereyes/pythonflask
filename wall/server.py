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

    query = 'SELECT * FROM users where email = :semail' #For verifying if email exists in database
    data = {'semail': request.form['email']}
    emails = mysql.query_db(query, data)

    if len(emails) > 0:
        flash("Email already exists")
    else:
        count +=1

    if count == 6:
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (:sfname, :slname, :semail, :spw)'
        data = {
            'sfname': request.form['fname'],
            'slname': request.form['lname'],
            'semail': request.form['email'],
            'spw': md5.new(request.form['pword']).hexdigest()
            }
        mysql.query_db(query, data)
        flash('Thanks for submitting your application')

        data2 = {'boom': request.form['email']} #Setting session id to registered user
        query2 = 'SELECT id, first_name FROM users WHERE email = :boom'
        ideez = mysql.query_db(query2, data2)
        session['id'] = ideez[0]['id']
        session['fname'] = ideez[0]['first_name']
        return redirect('/wall')
    else:
        return redirect('/')

@app.route('/log', methods=['POST'])
def eskitiit():
    password = md5.new(request.form['pword1']).hexdigest()
    email = request.form['email1']
    user_query = "SELECT * FROM users where users.email = :email AND users.password = :password"
    query_data = { 'email': email, 'password': password}
    user = mysql.query_db(user_query, query_data)

    

    if len(user) > 0:
        data2 = {'boom': request.form['email1']}
        query2 = 'SELECT id, first_name FROM users WHERE email = :boom'
        ideez = mysql.query_db(query2, data2)
        session['id'] = ideez[0]['id']
        session['fname'] = ideez[0]['first_name']
        return redirect('/wall')
    else:
        flash("Invalid Credentials")
        return redirect('/')

@app.route('/logout')
def bebye():
    session['id'] = 0
    return redirect('/')

@app.route('/wall')
def yo():
    # query = "SELECT users.id, users.first_name, users.last_name, messages.id, date_format(messages.created_at, '%M %d %Y' ) as msgdate, messages.message FROM messages JOIN users ON messages.id = users.id"
    # messages = mysql.query_db(query)
    query = "SELECT id, date_format(created_at, '%M %d %Y' ) as msgdate, message, user_id FROM messages ORDER BY created_at DESC;"
    messages = mysql.query_db(query)

    query2 = "SELECT id, first_name, last_name from users"
    users = mysql.query_db(query2)

    query3 = "SELECT id, comment, date_format(created_at, '%M %d %Y' ) as msgdate, message_id, user_id from comments"
    comments = mysql.query_db(query3)
    return render_template('wall.html', msgs=messages, usrs=users, cmnts = comments)

@app.route('/pstmsg', methods=['POST'])
def pstmsg():
    if len(request.form['msg']) < 1:
        flash("Message box is empty!")
    else:
        query = "INSERT INTO messages (message, user_id) VALUES (:msg, :uid)"
        data = {
            'msg': request.form['msg'],
            'uid': session['id']        
            }
        mysql.query_db(query, data)
    return redirect('/wall')

@app.route('/pstcmnt', methods=['POST'])
def pstcmnt():
    if len(request.form['cmnt']) < 1:
        flash("Message box is empty!")
    else:
        query = "INSERT INTO comments (comment, user_id, message_id) VALUES (:msg, :uid, :msgid)"
        data = {
            'msg': request.form['cmnt'],
            'uid': session['id'],
            'msgid': request.form['msgid']        
            }
        mysql.query_db(query, data)
    return redirect('/wall')
app.run(debug=True)
