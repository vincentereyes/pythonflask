from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'motorsport'

@app.route('/')
def index():
	if 'rand' not in session:
		session['rand'] = random.randrange(0, 101)
	print session['rand'] 
	return render_template("index.html")

@app.route('/guess', methods=['POST'])
def leggo():
	session['result'] = ""
	if session['rand'] > int(request.form['inp']):
		session['result'] = "Num too small"
	elif session['rand'] < int(request.form['inp']):
		session['result'] =  "Num too big"
	else:
		session['result'] = "u were ryt"

	return redirect('/')
@app.route('/reset', methods=['POST'])
def gogo():
	session['rand'] = random.randrange(0, 101)
	return redirect('/')
app.run(debug=True)

	
