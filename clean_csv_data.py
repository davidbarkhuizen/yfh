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

# -------------------------------------------------------------

def clean_csv_data_file_tree(root_folder):

	symbol_filepaths = get_symbols_with_filepath(root_folder)
	random.shuffle(symbol_filepaths)

	count = 0
	for (symbol, symbol_file_path) in symbol_filepaths:
	
		log(symbol)
	
		count += 1     
		timer_start = time.clock()      

  		csv_file_exists = CSV.file_exists(symbol_file_path)
  
  		if not csv_file_exists:
			log('no csv file found')
			continue

		log('csv file %s exists' % symbol_file_path)
		
		text = ''
		with open(symbol_file_path, 'rt') as csv_file:
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
		with open(symbol_file_path, file_access_mode) as out_file:
			out_file.write(out_text)
		
		print(symbol_file_path)
  
def main():
	log('root path = %s' % CSV_ROOT_PATH)
	#clean_csv_data_file_tree(CSV_ROOT_PATH)

	print(get_symbols_with_filepath(CSV_ROOT_PATH))
  
if __name__ == '__main__':
	main()