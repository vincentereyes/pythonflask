from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/survey', methods=['POST'])
def subform():
	name = request.form['name']
	loc = request.form['loc']
	lang = request.form['lang']
	com = request.form['com']
	return render_template("result.html", name = name, loc = loc, lang = lang, com = lang)

@app.route('/back')
def goback():	
	return redirect('/')

app.run(debug=True)