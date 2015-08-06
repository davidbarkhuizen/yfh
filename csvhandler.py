# csvhandler - david.barkhuizen@gmail.com - 2010-09-06 -> 2011-01-15
import csv
import datetime
from decimal import *

DATE_IDX = 0
OPEN_IDX = 1
HIGH_IDX = 2
LOW_IDX = 3
CLOSE_IDX = 4
VOL_IDX = 5
ADJ_CLOSE_IDX = 6

class CSV(object):
  
  @classmethod
  def file_exists(cls, file_path):
    try:
      f = open(file_path, 'r')
    except: # FileNotFoundException
      return False
    f.close()
    return True

  @classmethod
  def get_date_range(cls, file_path):
    '''
    return (start_date, end_date) for csv data rows @ file_path
    '''    
    slist = CSV.get_csv_as_sorted_list_of_dicts(file_path)
    return (slist[0]['date'], slist[len(slist) - 1]['date'])

  @classmethod
  def load_csv_list_from_file(cls, file_path):
    '''
    '''
    f = open(file_path, 'r')
    line = f.readline()
    f.close()
    splut = line.split(',')
    tokens = []
    for token in splut:
      cleaned = token.strip()
      if len(cleaned) > 0:
        tokens.append(cleaned)
    return tokens
  
  @classmethod
  def parse_string_to_date(cls, date_str):
    '''parse date string of format yyyy-mm-dd to datetime.date'''
    
    split_chars = ['-', '\\', '/', '.']
    split_char = '-'
    for char in split_chars:
      if (date_str.find(char) != -1):
        split_char = char
        break

    try:  
      tokens = date_str.split(split_char)
      y = int(tokens[0].lstrip('0'))
      m = int(tokens[1].lstrip('0'))
      d = int(tokens[2].lstrip('0'))
      return datetime.date(year=y, month=m, day=d)  
    except Exception, e:
      return None  
      
  @classmethod    
  def row_to_dict(cls, row):
    '''
    return dict with keys [date, open, high, low, close, volume, adj_close]
    '''
    try:
      date = CSV.parse_string_to_date(row[DATE_IDX])
    except IndexError:
      print(row)
      raise Exception()    
    
    if (date == None):
      return None

    open = Decimal(row[OPEN_IDX])
    high = Decimal(row[HIGH_IDX])
    low = Decimal(row[LOW_IDX])
    close = Decimal(row[CLOSE_IDX])

    try:
      volume = Decimal(row[VOL_IDX])
    except:
      volume = 0

    try:
      adj_close = Decimal(row[ADJ_CLOSE_IDX])
    except:
      adj_close = 0

    return {'date' : date, 'open' : open, 'high' : high, 'low' : low, 'close' : close, 'adj_close' : adj_close, 'volume' : volume }

  @classmethod
  def load_csv_data_rows(cls, file_path):
    '''
    load specified csv file, return list of rows (including header row, if any)
    '''
    
    data_rows = []
    line_count = 0  
    reader = None
    file = None
    
    exit_loop = False;
    while exit_loop == False:
      try:
        if (file == None):
          file = open(file_path, 'r')
          reader = csv.reader(file)  
      except Exception as e:        
        return None    
      try:
        row = reader.next()
        if (len(row) != 0):
          data_rows.append(row)
        line_count += 1
      except StopIteration:
        exit_loop = True

    if file != None:
      file.close()
    return data_rows

  @classmethod
  def rows_to_dicts(cls, rows):
    dicts = []
    for r in rows:
      dict = CSV.row_to_dict(r)
      if (dict != None):
        dicts.append(dict)
    return dicts
    
  @classmethod  
  def parse_rows_to_distinct_lists(cls, data_rows, clip_first_line=True):
    '''
    return (date, open, high, low, close, adj_close, volume) from list of data_rows
    '''

    date, open, high, low, close, adj_close, volume = [], [], [], [], [], [], []

    start_idx = 0
    if clip_first_line == True:
      start_idx = 1

    for i in range(start_idx, len(data_rows)):

      row_data = CSV.row_to_dict(data_rows[i])

      date.append(row_data['date'])
      open.append(row_data['open'])
      high.append(row_data['high'])
      low.append(row_data['low'])
      close.append(row_data['close'])
      adj_close.append(row_data['adj_close'])
      volume.append(row_data['volume'])    

    return date, open, high, low, close, adj_close, volume
  
  @classmethod  
  def get_csv_as_sorted_list_of_dicts(cls, file_path):
      raw_rows = CSV.load_csv_data_rows(file_path)
      dicts = CSV.rows_to_dicts(raw_rows)    
      sorted_dicts = sorted(dicts, key=lambda k: k['date'])    
      return sorted_dicts

  @classmethod
  def construct_date_dict(cls, list_of_dayinfo):
    d = {}
    for pinfo in list_of_dayinfo:
      d[pinfo['date']] = pinfo
    return d

#~ def PriceDataSource(Object):
  #~ def __init__(self, file_path):
    #~ # load data as sorted dicts
    #~ # build hastable index lookup
    #~ pass
  #~ def day(self, date):
    #~ pass
  #~ def period(self, start_date, end_date):
    #~ pass
