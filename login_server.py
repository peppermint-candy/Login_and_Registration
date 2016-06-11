from flask import Flask, render_template, request, session, redirect, flash
# import the Connector function
from flask.ext.bcrypt import Bcrypt
from LnR_mysqlconnection import MySQLConnector
import re
import md5

app = Flask(__name__)
mysql = MySQLConnector(app, 'assg_login_register')
app.secret_key = "Secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')
NAME = re.compile(r'[0,1,2,3,4,5,6,7,8,9]')
bcrypt = Bcrypt(app)

@app.route('/')
def index():
	return render_template('login_index.html')

@app.route('/register', methods=["POST"])
def process():

	if len(request.form['email']) < 1:
		flash("Email cannot be blank!")
		error = False
    # else if email doesn't match regular expression display an "invalid email address" message
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
		error = False
	else:
		error = True
	
	if len(request.form['pw']) < 8:
		flash("Password has to be longer than 8 characters")
		error = False
	elif request.form['pw'] != request.form['c_pw']:
		flash("Password and Confirm Password does not macth, Try again.")
		error = False
	else:
		error = True


	if len(request.form['first_name']) < 1:
		flash("First Name must have at least 2 characters")	
		error = False
	elif NAME.search(request.form['first_name']):
		flash("First Name cannot contain number(s)")
		error = False
	else:
		error = True

	if len(request.form['last_name']) < 1:
		flash("Last Name must have at least 2 characters")	
		error = False
	elif NAME.search(request.form['last_name']):
		flash("Last Name cannot contain number(s)")
		error = False
	else:
		error = True

	if error:
		flash("Thanks for submitting your information!")
		return create(request.form)
	else:
		flash("please validate your input")
		return redirect('/')

# @app.route('/create')
def create(data):

	pw = data['pw']
	print pw
	pw_hash = bcrypt.generate_password_hash(pw)

	insert_query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :pw, NOW(), NOW())"

	query_data = { 'first_name': data['first_name'], 'last_name': data['last_name'], 'email': data['email'], 'pw': pw_hash }

	mysql.query_db(insert_query, query_data)
	return redirect('/login')

@app.route('/loginX', methods=['POST'])
def logintab():
	elogin = request.form['elogin']
	Lpw = request.form['Lpw']

	user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
	query_data = {'email' : elogin}
	user = mysql.query_db(user_query, query_data)
	if bcrypt.check_password_hash(user[0]['password'], Lpw):
		print "successulf login"
		return redirect('/login')

	else:
		flash("Please try again")
		return	redirect('/')



@app.route('/login')
def login():
	print "Hello"
	return redirect('/')
app.run(debug=True)
