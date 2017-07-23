'''


fetch config from file/sql db
persist info to file/sql db

rotate fetching
log info, warnings, errors to file
single process
sql orm ? suitable for bulk inserts ? sqlalchemy ?
'''


# load config from .ini file

from config import load_or_create_config

CONFIG_FILE_NAME = 'yfh.ini'
config = load_or_create_config(CONFIG_FILE_NAME)