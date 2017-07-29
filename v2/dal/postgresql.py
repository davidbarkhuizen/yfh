# sudo apt-get install python3-psycopg2

import psycopg2
from collections import namedtuple

def configure(creds):
	
	connection_format = 'host={0} dbname={1} user={2} password={3}'
	connection_string = connection_format.format(creds.host, creds.database, creds.user, creds.password)
	
	def new_connection():
		return psycopg2.connect(connection_string) 

	connection = new_connection()

	def new_cursor():
		return connection.cursor()

	return new_cursor

# ----------------------------------------------------------------------