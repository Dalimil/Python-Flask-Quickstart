from flask import Flask
from flask import render_template, request, redirect, session, url_for, escape, make_response, flash, abort

app = Flask(__name__)
# (session encryption) keep this really secret:
app.secret_key = "bnNoqxXSgzoXSOezxpZjb8mrMp5L0L4mJ4o8nRzn"


@app.route('/')
def index():
    if 'username' in session:
        name = session['username']
        print('Logged in as {}'.format(escape(name)))
        print(session)

    tokenCookie = request.cookies.get('token')
    print("cookie: "+tokenCookie)

    resp = make_response(render_template('index.html'))
    resp.set_cookie('token', '123456789')
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get POST data
        session['username'] = request.form['username']
        # TODO check credentials here
        # flash('Invalid credentials', "error_category")
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
    return render_template('profile.html', name=name)

@app.route('/error')
def error():
    abort(401)


if __name__ == '__main__':
    #host='0.0.0.0' only with debug disabled - security risk
    app.run(port=8080, debug=True) 