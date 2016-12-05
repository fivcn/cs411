"""
CS 411 Recipe Web App Project
Amanda Doss, Shi Jin, Anran Wang, Lida Karadimou
"""

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login

#for image uploading
from werkzeug import secure_filename
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'pass' #change this

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass' #change this
app.config['MYSQL_DATABASE_DB'] = 'recipedb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users") 
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users") 
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd 
	return user


@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='login' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='password' id='password' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form></br>
		   <a href='/'>Home</a>
			   '''
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('home.html', message='Logged out') 

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html') 

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', supress=True)  

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def getUserFirstNameFromID(user_id):
	cursor = conn.cursor()
	cursor.execute("SELECT firstname FROM Users WHERE user_id = '{0}'".format(user_id))
	return cursor.fetchone()[0]

def getUserLastNameFromID(user_id):
	cursor = conn.cursor()
	cursor.execute("SELECT lastname FROM Users WHERE user_id = '{0}'".format(user_id))
	return cursor.fetchone()[0]


def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)): 
		#this means there are greater than zero entries with that email
		return False
	else:
		return True
#end login code

@app.route("/register", methods=['POST'])
def register_user():
	try:
		firstname = request.form.get('firstname')
		lastname = request.form.get('lastname')
		dateofbirth = request.form.get('dateofbirth')
		email=request.form.get('email')
		password=request.form.get('password')
	except:
		print ("couldn't find all tokens") #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print(cursor.execute("INSERT INTO Users (firstname, lastname, dateofbirth, email, password) VALUES ('{0}', '{1}','{2}','{3}','{4}')".format(firstname, lastname, dateofbirth, email, password)))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('home.html', name=firstname, message='Account Created!')
	else:
		print ("couldn't find all tokens")
		return flask.redirect(flask.url_for('register',message='ERROR!:User already exist'))

#following somebody
@app.route("/follow", methods= ['GET', 'POST'])
@flask_login.login_required
def follow_friend():
	if request.method == 'POST':
		user_id1 = getUserIdFromEmail(flask_login.current_user.id)
		email = request.form.get('email')
		test =  isEmailUnique(email)
		if not test:
			user_id2 = getUserIdFromEmail(email)
			print(email)
			cursor = conn.cursor()
			try:
				cursor.execute("INSERT INTO Follows (user_id1, user_id2) VALUES ('{0}', '{1}')".format(user_id1,user_id2))
				conn.commit()
				cursor.execute("INSERT INTO Follows (user_id1, user_id2) VALUES ('{0}', '{1}')".format(user_id2,user_id1))
				conn.commit()
				return render_template('home.html', name=flask_login.current_user.id, message='Friend Followed!')
			except:
				print ("already following this person")
				return render_template('follow.html', message='already following this person!!!!!!')
		else: 
			return render_template('home.html',name=flask_login.current_user.id, message='Sorry, user does not exist')
	else:
		return render_template('follow.html')

#add a new recipe, option available for logged in users only
@app.route('/add', methods=['GET', 'POST'])
@flask_login.login_required
def add_recipe():
	if request.method == 'POST':
		user_id = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		name = request.form.get('name')
		description = request.form.get('description')
		photo_data = base64.standard_b64encode(imgfile.read())
		cursor = conn.cursor()
		cursor.execute("INSERT INTO Recipe (imgdata, user_id, name, description) VALUES ('{0}', '{1}', '{2}', '{3}' )".format(photo_data,user_id, name, description))
		conn.commit()
		return render_template('home.html', name=flask_login.current_user.id, message='Recipe added!') #, recipes=getUsersRecipes(user_id) )
	else:
		return render_template('add.html')

		
#end recipe adding code code 	


#recipe searching code (we need to modify app routes according to front end pages)
@app.route("/recipesearch", methods = ['GET', 'POST'])
def recipesearch():
	searchentry = request.form.get('searchentry')
	allingredients = str(searchentry)
	ingredients = allingredients.split(' ')
	empty=[]
	q="SELECT recipe_id FROM Ingredient WHERE text = '" + (ingredients[0]) + "'"
	i=1
	while i < len(ingredients):
		q=q+" AND recipe_id IN (SELECT recipe_id FROM Ingredient WHERE text = '" + (ingredients[i]) +"' )"
		i=i+1
	return render_template('search.html', t=searchhelper(q))

def searchhelper(q):
	cursor = conn.cursor()
	cursor.execute(q)
	conn.commit
	return cursor.fetchall()


#end of searching for recipe code

@app.route("/addingredient", methods=['GET','POST'])
@flask_login.login_required
def addIngredient():  #request.form.get('text').split
	user_id = getUserIdFromEmail(flask_login.current_user.id)
	print(user_id)
	if request.method=='POST':
		recipe_id = request.form.get('recipe_id')
		text = request.form.get('text')   #request.form.get('text').split  kai meta size=length(tags) for i in length
		cursor = conn.cursor()          
		cursor.execute("SELECT * FROM Recipe WHERE user_id= '{0}' AND recipe_id = '{1}'".format(user_id,recipe_id))
		if (cursor.fetchone()==None):
			return render_template("addingredient.html", message="recipe does not exist or is not yours")
		else:
			cursor=conn.cursor()
			cursor.execute("INSERT INTO Ingredient ( text, recipe_id) VALUES ('{0}','{1}')".format( text , recipe_id))
			conn.commit()
			return render_template("addingredient.html",message="ingredient added, if you want add another one:")
	else:
		return render_template("addingredient.html")

#getting all the ingredients according to recipe id
def getIngredient(recipe_id):
	cursor=conn.cursor()
	cursor.execute("SELECT text FROM Ingredients WHERE recipe_id='{0}'".format(recipe_id))
	return cursor.fetchall() 

@app.route("/view_by_ingredient", methods=['GET','POST'])
def view_by_ingredient():
	text = request.form.get('text')
	return render_template("view_by_ingredient.html", recipe=getRecipebyIngredient(text) )

def getRecipebyIngredient(text):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata,name FROM (Recipe INNER JOIN Ingredient ON Recipe.recipe_id = Ingredient.recipe_id) WHERE text= '{0}'".format(text))
	return cursor.fetchall()


@app.route("/", methods=['GET'])
def home():
	return render_template('home.html', message='Welcome to our Recipe Web App!')



if __name__ == "__main__":
	#this is invoked when in the shell  you run 
	#$ python app.py 
	app.run(port=5000, debug=True)

