import sqlite3

def configure(database, user, password):
    
    connection_string = "dbname='{0}' user='{1}' password='password'".format(
    	database, user, password)
	
	def new_connection():
		return psycopg2.connect(connection_string) 

	connection = new_connection()

	def new_cursor():
		return connection.cursor()

	return new_cursor

# ----------------------------------------------------------------------

def get_symbol(cursor, id):

	cursor.execute('''select Code, Description from Symbols where Id = {0}'''.format(id))

	row = cur.fetchone()
	# rows = cur.fetchall()