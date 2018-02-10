from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def runindex():
	return render_template('index.html')

@app.route('/ninjas')
def runninja():
	return render_template('ninjas.html')

@app.route('/dojos/new')
def runform():
	return render_template('dojos.html')
app.run(debug=True)
