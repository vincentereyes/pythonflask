from flask import Flask, render_template, request, redirect, session, flash
import re

name_regex = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'motorsport'
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/formsub', methods=['POST'])
def lego():
	count = 0;
	if len(request.form['email']) < 1 or len(request.form['fname']) < 1 or len(request.form['lname']) < 1 or len(request.form['pword']) < 1 or len(request.form['cpword']) < 1:
		flash('Dont leave a field blank')
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

	if count == 5:
		flash('Thanks for submitting your application')
	return redirect('/')
app.run(debug=True)

