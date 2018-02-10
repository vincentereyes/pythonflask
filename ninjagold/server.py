from flask import Flask, render_template, request, redirect, session, flash
import random
app = Flask(__name__)
app.secret_key = 'motorsport'

@app.route('/')
def index():
	if 'gold' not in session:
		session['gold'] = 0
	return render_template("index.html")

@app.route('/process_money', methods=['POST'])
def game():
	session['prize'] = 0
	if 'logg' not in session:
		session['logg'] = []
	if request.form['building'] == 'farm':
		session['prize'] = random.randrange(10, 21)
		session['logg'].append("Earned " + str(session['prize']) + " gold from the farm!")
		print session['logg']
	elif request.form['building'] == 'cave':
		session['prize'] = random.randrange(5, 11)
		session['logg'].append("Earned " + str(session['prize']) + " gold from the cave!")
	elif request.form['building'] == 'house':
		session['prize'] = random.randrange(2, 6)
		session['logg'].append("Earned " + str(session['prize']) + " gold from the house!")
	else:
		random_number = 0
		if random.random() < 0.5:
			random_number = -1
		else:
			random_number = 1
		print random_number
		session['prize'] = (random.randrange(0, 51) * random_number)
		if session['prize'] < 0:
			session['logg'].append("Lost " + str(session['prize']) + " gold from the casino!")
		else:
			session['logg'].append("Earned " + str(session['prize']) + " gold from the casino!")
	session['gold'] += session['prize']
	return redirect('/')

app.run(debug=True)