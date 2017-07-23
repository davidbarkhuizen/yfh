from pycore import configure_logging, log
configure_logging('csv_data_update.log')

# -------------------------------------------------------------

import time
import datetime
import sys

from csvhandler import CSV
from httpadaptor import *

ONE_DAY = datetime.timedelta(days=1) 
DELAY = 0.25

FOLDER_PATH = '/home/mage/data/csv_data_dec_2015/yahoo_finance/'

# -------------------------------------------------------------
import glob, os

def get_csv_file_paths(folder_path, wildcard):
	
	expression = os.path.join(folder_path, wildcard)
	return glob.glob(expression, recursive=True)

def clean_csv_data_file(file_path):

	csv_file_exists = CSV.file_exists(file_path)

	if not csv_file_exists:
		print('no csv file found')
		return

	text = ''
	with open(file_path, 'rt') as csv_file:
		text = csv_file.read()
	
	raw_lines = text.split('\n')

	cleaned_lines = []

	for raw_line in raw_lines:

		data = raw_line.split(',')

		if len(data) != 13:
			if len(data) > 1:
				cleaned_lines.append(raw_line)
		else:
			left = data[:6]
			middle = data[6]
			right = data[7:]

			middle_right = middle[-10:]
			middle_left = middle[:-10]

			left.append(middle_left)
			temp = [middle_right]
			temp.extend(right)
			right = temp

			cleaned_lines.append(','.join(left).replace('\r', ''))
			cleaned_lines.append(','.join(right).replace('\r', ''))

	out_text = '\n'.join(cleaned_lines)

	file_access_mode = 'wt' # 'at' if csv_file_exists else 'wt'
	with open(file_path, file_access_mode) as out_file:
		out_file.write(out_text)
	
	print(file_path)
  
def main():

	csv_file_paths = get_csv_file_paths(FOLDER_PATH, '**/*.csv')

	print('-----')
	print(csv_file_paths)

	for file_path in csv_file_paths: 
		print(file_path)
		clean_csv_data_file(file_path)

if __name__ == '__main__':
	main()