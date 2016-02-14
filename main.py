from flask import Flask
from flask import render_template, request, redirect, session, url_for, escape, make_response, flash, abort
import database

app = Flask(__name__)
# (session encryption) keep this really secret:
app.secret_key = "bnNoqxXSgzoXSOezxpZjb8mrMp5L0L4mJ4o8nRzn"

# SQL Alchemy database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # absolute
# also possible "mysql://username:password@server/db" (or postgresql)
database.db.init_app(app) # bind
database.db.create_all(app=app) # create tables

@app.route('/')
def index():
	if 'username' in session:
		name = session['username']
		print('Logged in as {}'.format(escape(name)))
		print(session)

	tokenCookie = request.cookies.get('token')
	print("cookie: "+str(tokenCookie))

	resp = make_response(render_template('index.html'))
	resp.set_cookie('token', '123456789')
	return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		# get POST data
		session['username'] = request.form['username']
		# TODO check credentials here
		# flash('Invalid credentials', "error_category"); abort(401)
		# # and no redirect OR success:
		flash('You were successfully logged in')
		return redirect(url_for('index'))
	else: 
		# get GET data /login?attemptCount=3&showAd=false
		attemptCount = request.args.get('attemptCount', '0'); #default value
		print("attempts:"+str(attemptCount))

	# return app.send_static_file('login_static.html') # we can also use static folder
	return render_template('login.html')

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/user/<name>')
def show_profile(name=None):
	# name is a variable obtained from the url path
	database.add_user(name, "1234-"+name)
	print(database.get_users()) 
	return render_template('bootstrap_example.html', name=name)


# Flask-SocketIO -------------------------------------------------------
@app.route('/socket_index')
def my_socket_page():
	return render_template('sockets_example.html')

from flask_socketio import SocketIO, send, emit
# WebSockets setup -- "https://flask-socketio.readthedocs.org/en/latest/"
# See docs for 'rooms' - join/leave etc.
socketio = SocketIO(app)
# SocketIO RECEIVE and SEND Messages
# Originating from a user
@socketio.on('user_clicked_button') # CUSTOM or use predefined 'json', or 'message' (for strings)
def handle_my_custom_event(arg1, arg2): # any number of args
    print(arg1); print(arg2)
    print(session)
    emit('all_ok', "You sent me this:"+arg2) # broadcast=True

# Originating from this server
def some_internal_function():
	# different emit()/send() (notice 'socketio' prefix)
    socketio.emit('big_news', {'data': 42}) # broadcast is implicit

# -------------------------------------------------------------------

if __name__ == '__main__':
	#host='0.0.0.0' only with debug disabled - security risk
	#app.run(port=8080, debug=True) - don't use this one with sockets
	socketio.run(app, port=8080, debug=True) # only use this with sockets