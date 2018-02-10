from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/ninja')
def blabla():
	return render_template("ninja.html", path="tmnt.png")

@app.route('/ninja/<color>')
def show(color):
	a = ""
	if color == "blue":
		a = "leonardo.jpg"
	elif color == "red":
		a = "raphael.jpg"
	elif color == "orange":
		a = "michelangelo.jpg"
	elif color == "purple":
		a = "donatello.jpg"
	else:
		a = "notapril.jpg"
	return render_template("ninja.html", path=a)
	
app.run(debug=True)