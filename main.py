from flask import Flask
from flask import render_template, request, redirect, session, url_for, escape, make_response

app = Flask(__name__)
# (session encryption) keep this really secret:
app.secret_key = "bnNoqxXSgzoXSOezxpZjb8mrMp5L0L4mJ4o8nRzn"


@app.route('/')
def index():
    if 'username' in session:
    	name = session['username']
        return 'Logged in as {}'.format(escape(name))

    tokenCookie = request.cookies.get('token')
    print(tokenCookie)

    resp = make_response(render_template('index.html'))
    resp.set_cookie('token', '123456789')
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    	# get POST data
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:    	
    	# get GET data /login?attemptCount=3&showAd=false
    	print(request.args.get('attemptCount', ''))

    return send_static_file('login.html') # static folder

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/user/<name>')
def show_profile(name=None):
	# name is a variable obtained from the url path
	return render_template('hello.html', name=name)

@app.route('/error')
def error():
	abort(401)


if __name__ == '__main__':
	#host='0.0.0.0' only with debug disabled - security risk
    app.run(port=8080, debug=True) 