import os.path
import configparser

template = {

	'database' : {  

		'host':'host',
		'database':'pricedata',
		'user':'',
		'password':'' 
		
		}	
}

def create_config_file_from_template(file_path):

	parser = configparser.ConfigParser()

	for key in template:
		parser[key] = template[key]

	with open(file_path, 'w') as config_file:
		parser.write(config_file)

def load_config_from_file(config_file_path):

	config = configparser.ConfigParser()
	config.read(config_file_path)

	return config

def load_or_create_config(config_file_path):

	if not os.path.isfile(config_file_path):
		print('no configuration file found @ {0}'.format(config_file_path))

		create_config_file_from_template(config_file_path)
		print('new configuration file created @ {0}'.format(config_file_path))

		return None
	
	return load_config_from_file(config_file_path)