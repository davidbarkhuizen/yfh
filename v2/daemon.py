'''
fetch config from file/sql db
persist info to file/sql db

rotate fetching
log info, warnings, errors to file
single process
sql orm ? suitable for bulk inserts ? sqlalchemy ?
'''

# ----------------------------------------------------------------------
# load config from .ini file

from config import load_or_create_config

CONFIG_FILE_PATH = 'yfh.ini'

config = load_or_create_config(CONFIG_FILE_PATH)

if not config: 
	print('populate the config file settings and retry')
	exit(1)

# ----------------------------------------------------------------------

from dal import postgresql, model

db_config = config['database']

credentials = model.Credential(
	host=config['database']['host'],
	user=config['database']['user'], 
	password=config['database']['password'], 
	database=config['database']['database']
	)
new_cursor = postgresql.configure(credentials)

cursor = new_cursor()










