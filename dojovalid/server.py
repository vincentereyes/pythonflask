from flask import Flask, render_template, request, redirect, session, flash
import random
app = Flask(__name__)
app.secret_key = 'motorsport'
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/survey', methods=['POST'])
def lego():
	if len(request.form['name']) < 1:
		flash("Name cannot be empty")
	if len(request.form['com']) > 120:
		flash("Comment field exceeded limit of 120 characters")
	elif len(request.form['com']) < 1:
		flash("Comment field cannot be left blank")
	return redirect('/')

app.run(debug=True)