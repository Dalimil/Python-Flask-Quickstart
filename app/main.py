from flask import *
# Import the database and app object from the main app module
from app import app, db
# Import module models (i.e. User)
from app.models import User

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


# ---------------- Flask-SocketIO ----------------------------
@app.route('/socket_index')
def my_socket_page():
	return render_template('sockets_example.html')

from app import socketio
from flask_socketio import send, emit

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


# ---------------- DATABASE ------------------------
import hashlib

def hash(data):
    return hashlib.sha256(str(data)).hexdigest()

# INSERT
def add_user(username, password):
    new_user = User('guest', hash('123456789'))
    db.session.add(new_user) # delete works similarly
    db.session.commit()
    print(new_user.id)

# QUERY
def get_users():
    users = User.query.all()
    # More examples:
    guest = User.query.filter_by(username='guest').first()
    if guest != None:
        print(guest.username)

    User.query.filter(User.username.endswith('st')).order_by(User.username).limit(2).all()
    primary_key = 1
    User.query.get(primary_key)

    return users