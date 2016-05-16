# Import the database object (db) from the application module - see /app/__init__.py
from app import db

# Define a base model for other database tables to inherit
# Types are: Integer, String(maxLen), Text, DateTime, Float, PickleType, LargeBinary
# Relationships: http://flask-sqlalchemy.pocoo.org/2.1/models/

class Base(db.Model):
    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class User(Base): # inherit Base
    __tablename__ = 'auth_user' # optional
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self): # optional
        return '<User %r>' % (self.username)    

