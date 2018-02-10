from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'isitreallyasecret'
@app.route('/')
def index():
	if 'count' in session:
		session['count'] += 1	
	else:
		session['count'] = 1
	return render_template("index.html")
app.run(debug=True)