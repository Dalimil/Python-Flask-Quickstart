from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported by modules and controllers
db = SQLAlchemy(app)

# WebSockets setup -- "https://flask-socketio.readthedocs.org/en/latest/"
from flask_socketio import SocketIO
socketio = SocketIO(app)

# Import modules

import main

# Register blueprint(s) - (but need to import first)
# app.register_blueprint(auth_module)
# ..

# Build the database - (create the database file using SQLAlchemy)
db.create_all()