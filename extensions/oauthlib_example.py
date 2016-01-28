from flask_oauthlib.client import OAuth

oauth = OAuth(app) # or oauth = oAuth(); oauth.init(app) for later init

# Twitter
the_remote_app = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='<your key here>',
    consumer_secret='<your secret here>'
)

## ...or Facebook
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='<facebook app id>',
    consumer_secret='<facebook app secret>',
    request_token_params={'scope': 'email'} # Facebook specific
)
#######

@app.route('/login')
def login():
	next_url = request.args.get('next') or request.referrer or None
    return twitter.authorize(callback=url_for('oauth_authorized', #redirect back to this url
        next=next_url))

@app.route('/login/oauth-authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')
    resp = twitter.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        # 'Access denied: reason={} error={}'.format(request.args['error'], request.args['error_description'])
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    # In larger applications it is recommended to store satellite information in a database instead

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


# THE USER HAS SIGNED IN - CALL API NOW

# Create a tweet
resp = twitter.post('statuses/update.json', data={
    'status':   'The text we want to tweet'
})
if resp.status != 403:
    flash('Successfully tweeted your tweet (ID: #%s)' % resp.data['id'])

# Display user's feed
resp = twitter.get('statuses/home_timeline.json')
if resp.status == 200:
    tweets = resp.data