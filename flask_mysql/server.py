from flask import Flask
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql"; note that you pass the database name to the function
mysql = MySQLConnector(app, 'mydb')
# an example of running a query
data = mysql.query_db("SELECT * FROM users")

for x in range(0, len(data)):
	print data[x]['first_name'] + " " + data[x]['last_name']

app.run(debug=True)
