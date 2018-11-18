######################################
# author ben lawson <balawson@bu.edu> 
# Edited by: Craig Einstein <einstein@bu.edu>
# Edited by: Arshitha Basavaraj <arshitha@bu.edu>
######################################
# Some code adapted from 
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
#for image uploading
from werkzeug import secure_filename
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aaron27swartz' #CHANGE THIS TO YOUR MYSQL PASSWORD
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
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


'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''

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
	return render_template('hello.html', message='Logged out') 

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html') 

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier


# Becoming a Registered User
@app.route("/register/", methods=['GET'])
def register():

	return render_template('improved_register.html', supress='True')  

@app.route("/register/", methods=['POST'])
def register_user():
	try:
		email=request.form.get('email')
                print email
		password=request.form.get('password')
		getUserFirstName = request.form.get('firstname')
		last_name = request.form.get('lastname')
	except:
		print "couldn't find all tokens" #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print cursor.execute("INSERT INTO Users (getUserFirstName, last_name, email, password) VALUES ('{0}', '{1}','{2}','{3}')".format(getUserFirstName, last_name, email, password))

		conn.commit()
		uid = getUserIdFromEmail(email);
		print uid
		# cursor.execute("INSERT INTO profile_pic (user_id, profile_pic) VALUES ('{0}', LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg')".format(uid))
		# conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('profile.html', name=getUserFirstName, message='Account Created Successfully')
	else:
		print "couldn't find all tokens"
		return flask.redirect(flask.url_for('register'))

def getUsersPhotos(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, picture_id, caption FROM Pictures WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall() 

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
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

def getProfilePicture(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT profile_pic  FROM profile_pic WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

# profile of the user
@app.route('/profile')
@flask_login.login_required
def protected():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('profile.html', name=getUserFirstName(uid), message="Here's your profile")

def getUserFirstName(uid):
	cursor = conn.cursor()
	if cursor.execute("SELECT first_name FROM Users WHERE user_id='{0}'".format(uid)):
		return cursor.fetchall()[0][0]
	else:
		return None
# end profile code

# Gallery that lists all of the users photos
@app.route("/gallery", methods=['POST', 'GET'])
@flask_login.login_required
def all_pictures():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	pictures_list = []
	for each in getUsersPhotos(uid):
		pictures_list.append(each)
		print each
	# posting the collected pictures
	# print(pictures_list)
	if request.method == "GET":
		return render_template('gallery.html', message='Your Gallery', photos=getUsersPhotos(uid))

# Adding and Listing Friends Feature
@app.route('/friends', methods=['GET','POST'])
@flask_login.login_required
def friends():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	friends = getUserFriends(uid)
	print uid
	print friends
	friend_names = []
	for each in friends:
		friend_names.append(getUserFirstName(each))
		print friend_names
	if request.method == 'POST':
		first_name = request.form.get('first_name_query')
		last_name = request.form.get('last_name_query')
		if findFriends(first_name,last_name):
			return render_template('friends.html', friend_list=friend_names, other_users=findFriends(first_name,last_name))
		else:
			return render_template('friends.html', friend_list=friend_names, message="Please enter User's First Name or Last Name")
	else:
		return render_template('friends.html', friend_list=friend_names)

def getUserFriends(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT friend_id FROM friends WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall()

def findFriends(firstname, lastname):
	cursor = conn.cursor()
	first_name = str(firstname)
	last_name = str(lastname)
	
	if first_name != '' and last_name == '':
		cursor.execute("SELECT user_id, first_name, last_name, email FROM Users WHERE first_name = '{0}' ORDER BY user_id".format(first_name))
	elif first_name == '' and last_name != '':
		cursor.execute("SELECT user_id, first_name, last_name, email FROM Users WHERE last_name = '{0}' ORDER BY user_id".format(last_name))
	elif first_name != '' and last_name != '':
		cursor.execute("SELECT user_id, first_name, last_name, email FROM Users WHERE first_name = '{0}' AND  last_name = '{1}' ORDER BY user_id".format(first_name,last_name))
	return cursor.fetchall()

@app.route('/add_friends', methods=['GET','POST'])
@flask_login.login_required
def add_friends():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	friend_ids = getUserFriends(uid)
	print friend_ids
	friend_names = []
	for each in friend_ids:
		friend_names.append(getUserFirstName(uid))
		print friend_names
	if request.method == 'POST':
		email = request.form.get('user_email')
		for each in friend_ids:
			if each == getUserIdFromEmail(email):
				return render_template('add_friends.html', message = "already a friend", all_users= getAllUsers())
		if addFriend(uid,email):
			return render_template('add_friends.html', message=addFriend(uid,email), updated_friend_list=friend_names, all_users= getAllUsers())
		else:
			return render_template('add_friends.html', message="Email not found. Try Again.", updated_friend_list=[], all_users= getAllUsers())
	else:
		return render_template('add_friends.html', all_users= getAllUsers())

def addFriend(uid, email):
	cursor = conn.cursor()
	if getUserIdFromEmail(email):
		cursor.execute("INSERT INTO friends(user_id,friend_id) VALUES ('{0}','{1}')".format(uid, getUserIdFromEmail(email)))
		conn.commit()
		return "Successfully Added " + email
	else:
		return None

def getAllUsers():
	cursor = conn.cursor()
	cursor.execute("SELECT first_name, last_name, email FROM Users")
	return cursor.fetchall()

# end Adding and Listing Friends code

# Photo Upload
# photos uploaded using base64 encoding so they can be directly embeded in HTML 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		caption = request.form.get('caption')
		print caption
		photo_data = base64.standard_b64encode(imgfile.read())
		cursor = conn.cursor()
		cursor.execute("INSERT INTO Pictures (imgdata, user_id, caption) VALUES ('{0}', '{1}', '{2}' )".format(photo_data,uid, caption))
		conn.commit()
		return render_template('hello.html', name=getUserFirstName(uid), message='Photo uploaded Successfully', photos=getUsersPhotos(uid) )
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		return render_template('upload.html')
#end photo uploading code 

#default page
# this is where anonymous browsing happens  
@app.route("/", methods=['GET'])
def hello():
	return render_template('hello.html', message='Welcome to Photoshare')

if __name__ == "__main__":
	#this is invoked when in the shell  you run 
	#$ python app.py 
	app.run(port=5000, debug=True)
