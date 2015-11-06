from flask import Flask
from flask import render_template, request, redirect

app = Flask(__name__)

if __name__ == '__main__':
	#host='0.0.0.0' only with debug disabled - security risk
    app.run(port=8080, debug=True) 
