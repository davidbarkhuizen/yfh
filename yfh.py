from pycore import configure_logging, log
configure_logging('csv_data_update.log')

import time
import datetime
import sys

import random

from csvhandler import CSV
from httpadaptor import *

ONE_DAY = datetime.timedelta(days=1) 

WAIT_BETWEEN_SYMBOLS_S = 1
CSV_ROOT_PATH = '/home/mage/data/csv_data_dec_2015/'

NETWORK_RETRY_LIMIT = 1000
NETWORK_RETRY_WAIT_S = 1 

# -------------------------------------------------------------

def get_symbols_with_filepath(root_folder):

	symbol_filepath = []

	symbol_types_list_file_path = root_folder + 'symbol_types' + '.csv'
	symbol_types = CSV.load_csv_list_from_file(symbol_types_list_file_path)
  
	for symbol_type in symbol_types:
		
		folder = root_folder + symbol_type + '/'
		symbol_list_file_path = folder + 'symbols' + '.csv'
		symbols = CSV.load_csv_list_from_file(symbol_list_file_path)
	
		for symbol in symbols:
	  		symbol_file_path = folder + symbol + '.csv'

	  		symbol_filepath.append((symbol, symbol_file_path))

	return symbol_filepath

# -------------------------------------------------------------

def update_csv_to_present_from_net(root_folder):
	'''
	load first line of text file 'symbol_types.csv' @ CSV_ROOT_PATH
	assume line to be csv values, split into string list of symbol types
	assume that CSV_ROOT_PATH contains a direct subfolder for each symbol type
	and that each subfolder contains a symbols.txt text file 
	with the first line being a csv list of symbols

	'''  

	symbol_filepaths = get_symbols_with_filepath(root_folder)
	random.shuffle(symbol_filepaths)

	count = 0
	for symbol, symbol_file_path in symbol_filepaths:
		
		log('-'*80)
		log('{0} - {1}'.format(symbol, symbol_file_path))
		
		count += 1     
		timer_start = time.clock()      
  
  		csv_file_exists = CSV.file_exists(symbol_file_path)
  
  		if (csv_file_exists == True):
			log('csv file %s exists' % symbol_file_path)
			try:
				(d_start, d_end) = CSV.get_date_range(symbol_file_path)
			except Exception, e:
				log('exception encountered while examining existing data file, skipping symbol')
				continue

			log('existing data spans range %s - %s' % (str(d_start), str(d_end)))
			i = d_end + ONE_DAY        
  		else:
			log('no csv file found')
			i = datetime.date(year=1900,month=1,day=1)    
	
  		f = datetime.datetime.now()

  		if (i.year == f.year) and (i.month == f.month) and (i.day == f.day):
			log('stored data is current')
			continue # to next symbol

		body = None

		msg = 'requesting data from {0}-{1}-{2} to {3}-{4}-{5}'.format(
			str(i.year).zfill(2), str(i.month).zfill(2), str(i.day).zfill(2),
			str(f.year).zfill(2), str(f.month).zfill(2), str(f.day).zfill(2)
			) 
		log(msg)

		retry_count = 0

		while retry_count < NETWORK_RETRY_LIMIT:

			try:

				body = get_csv_lines_for_period(symbol,
					str(i.year).zfill(2), str(i.month).zfill(2), str(i.day).zfill(2),
					str(f.year).zfill(2), str(f.month).zfill(2), str(f.day).zfill(2)
					)

				break

			except Exception, e:

				retry_count = retry_count + 1
				log('attempt %i to fetch data failed: %s' % (retry_count, str(e)))

				if retry_count < NETWORK_RETRY_LIMIT:
					log('sleeping for %i seconds before retrying')
					time.sleep(NETWORK_RETRY_WAIT_S)

		data_lines = body.split('\n')[1:-1]
		log('# of data lines returned = %s' % str(len(data_lines)))

		to_sort = []

		for line in data_lines:

			row = line.split(',')
		 	d = CSV.row_to_dict(row)

		  	if d is None:
		  		continue
  
		  	is_valid = d['date'] > d_end if csv_file_exists else True 
		  
			if not is_valid:
				continue
				
			datum = {
				'line' : line,
				'date' : d['date']
				}
			to_sort.append(datum)
		
		seq = sorted(to_sort, key=lambda j:j.get('date'))	  
	
		file_access_mode = 'at' if csv_file_exists else 'wt'
		new_text = '\n'.join([x['line'] for x in seq])
		with open(symbol_file_path, file_access_mode) as out_file:
			out_file.write(new_text)
		
		timer_end = time.clock()
		
		log('{0} [{1} / {2}] in {3} seconds'.format(symbol, count, len(symbol_filepaths), timer_end - timer_start))
		
		log('sleeping for %i seconds before next symbol' % WAIT_BETWEEN_SYMBOLS_S)
		time.sleep(WAIT_BETWEEN_SYMBOLS_S) 
  
def main():	

	log('root path = %s' % CSV_ROOT_PATH)
	update_csv_to_present_from_net(CSV_ROOT_PATH)
  
if __name__ == '__main__':
	main()