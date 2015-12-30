import sqlite3
import hashlib
import os

def getConnection():
	sqlite_file = "sqlite_database.db"

	## Openshift fix
	#if('OPENSHIFT_DATA_DIR' in os.environ):
	#	sqlite_file = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'sqlite_database.db')

	if not os.path.isfile(sqlite_file):
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()
		c.execute("CREATE TABLE Users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT );") 
		# c.execute("CREATE TABLE ... ")
		conn.commit()
		conn.close()
		
	return sqlite3.connect(sqlite_file)

def selectUsers(name):
	conn = getConnection()
	c = conn.cursor()
	c.execute("SELECT * FROM Users WHERE name = '{}' ".format(name))
	res = c.fetchall()
	conn.commit()
	conn.close()
	return res

def addUser(data):
	conn = getConnection()
	c = conn.cursor()
	c.execute("INSERT INTO Users (name, password) VALUES ('{}', '{}')".format(data["name"], hashlib.sha256(data["passw"]).hexdigest()))
	# c.execute("INSERT INTO ...")
	conn.commit()
	conn.close()
