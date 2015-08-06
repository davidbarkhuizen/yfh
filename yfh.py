import logging
LOG_FILENAME = 'csv_data_update.log'
FORMAT = "%(message)s"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=FORMAT)

def log(s):
  print(s)
  logging.info(s)

#-------------
import time
import datetime
import sys
#-------------
from csvhandler import CSV
from httpadaptor import *
# -------------------------------------------
ROOT_PATH = '/home/david/data/csv_data/'
ONE_DAY = datetime.timedelta(days=1) 
DELAY = 0.25

def s(i):
  '''
  left-pad strings of length 1 with a '0' char
  otherwise return the string 
  '''
  st = str(i)
  if len(st) == 1:
    return '0' + st
  return st

def update_csv_to_present_from_net(root_folder):
  '''
  load first line of text file 'symbol_types.csv' @ ROOT_PATH
  assume line to be csv values, split into string list of symbol types
  assume that ROOT_PATH contains a direct subfolder for each symbol type
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
    # load csv list of symbols from file 'symbols.csv' in subfolder (with name of symbol type) of root folder
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
        continue
 
      body = None
      try:
        log('requesting data from %s-%s-%s to %s-%s-%s' % (s(i.year), s(i.month), s(i.day), s(f.year), s(f.month), s(f.day)))
        body = get_csv_lines_for_period(symbol, s(i.year), s(i.month), s(i.day), s(f.year), s(f.month), s(f.day))
        
        lines = body.split('\n')
        lines = lines[1:len(lines)-1]            
        log('# of data lines returned = %s' % str(len(lines)))
        
        to_sort = []
        
        for line in lines:
        
          row = line.split(',')
          d = CSV.row_to_dict(row)
          
          is_valid = False
          
          if (csv_file_exists == True):
            if (d['date'] > d_end):
              is_valid = True
            else:
              is_valid = False
          else:
            is_valid = True        
          
          if is_valid == True:
            ob = {}
            ob['line'] = line
            ob['date'] = d['date']
            to_sort.append(ob)
        
        if len(to_sort) > 1:
          seq = sorted(to_sort, key=lambda j:j.get('date'))
        else:
          seq = to_sort
      except Exception as e:
        log(str(e))
        print('failed')
        continue
        
      f = None
      if csv_file_exists == True:
        f = open(symbol_file_path, 'a')
      else:
        f = open(symbol_file_path, 'w')        
      for d in seq:
        f.write(d['line'] + '\n')      
      f.close()      
      timer_end = time.clock()
      print('symbol %s [%s / %s] in %s seconds' % (symbol, str(count), str(len(symbols)), str(timer_end - timer_start)))
      time.sleep(DELAY) 
  
def main():
  log('root path = %s' % ROOT_PATH)
  update_csv_to_present_from_net(ROOT_PATH)
  
if __name__ == '__main__':
  main()

