import logging
import time
import datetime
import sys

from csvhandler import CSV
from httpadaptor import *

ONE_DAY = datetime.timedelta(days=1) 

WAIT_BETWEEN_SYMBOLS_S = 10
LOG_FILENAME = 'csv_data_update.log'
LOG_FORMAT = "%(message)s"
CSV_ROOT_PATH = '/home/mage/data/csv_data_dec_2015/'

NETWORK_RETRY_LIMIT = 1000
NETWORK_RETRY_WAIT_S = 60 

# -------------------------------------------------------------
# LOGGING -----------------------------------------------------

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=LOG_FORMAT)

def log(s):
	print(s)
	logging.info(s)

# -------------------------------------------------------------

def update_csv_to_present_from_net(root_folder):
	'''
	load first line of text file 'symbol_types.csv' @ CSV_ROOT_PATH
	assume line to be csv values, split into string list of symbol types
	assume that CSV_ROOT_PATH contains a direct subfolder for each symbol type
	and that each subfolder contains a symbols.txt text file 
	with the first line being a csv list of symbols

	'''  

	# load csv list of symbol types from file 'symbol_types.csv' in root folder
	symbol_types_list_file_path = root_folder + 'symbol_types' + '.csv'
	log('loading csv list of symbol types @ %s' % symbol_types_list_file_path)
	try:
		symbol_types = CSV.load_csv_list_from_file(symbol_types_list_file_path)
		log('ok')
	except Exception, e:
		log('exception - %s' % str(e))
		return
  
	for symbol_type in symbol_types:
		
		folder = root_folder + symbol_type + '/'
		symbol_list_file_path = folder + 'symbols' + '.csv'
		log('loading csv list of symbols @ %s' % symbol_list_file_path)
		symbols = CSV.load_csv_list_from_file(symbol_list_file_path)
		log('ok')
	
		count = 0
		for symbol in symbols:
			
			log(symbol)
			
			count += 1     
			timer_start = time.clock()      
	  
	  		symbol_file_path = folder + symbol + '.csv'
	  		csv_file_exists = CSV.file_exists(symbol_file_path)
	  
	  		if (csv_file_exists == True):
				log('csv file %s exists' % symbol_file_path)
				(d_start, d_end) = CSV.get_date_range(symbol_file_path)
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
			
			print('symbol %s [%s / %s] in %s seconds' % (symbol, str(count), str(len(symbols)), str(timer_end - timer_start)))
			time.sleep(WAIT_BETWEEN_SYMBOLS_S) 
  
def main():
	log('root path = %s' % CSV_ROOT_PATH)
	update_csv_to_present_from_net(CSV_ROOT_PATH)
  
if __name__ == '__main__':
	main()