# 2010-07-17 - 2011-01-16 @ david barkhuizen
# yahoo finance harvester component

import http.client
http.client.HTTPConnection.debuglevel = 0
import urllib

URL_STEM = 'http://ichart.finance.yahoo.com/table.csv?'

def construct_ichart_csv_url(symbol, fromY, fromM, fromD, toY, toM, toD):
  '''
  ('BP', '1900', '01', '01', '2010', '07', '18')
  '''
  q = dict()
  
  q['s'] = symbol
  
  q['a'] = str(int(fromM) - 1)
  q['b'] = fromD
  q['c'] = fromY
  q['d'] = str(int(toM) - 1)
  q['e'] = toD
  q['f'] = toY
  q['g'] = 'd'
  
  # valid example as @ 2011/01/16
  # http://ichart.finance.yahoo.com/table.csv? s=JPM &a=11 &b=30 &c=1983 &d=00 &e=16 &f=2011 &g=d &ignore=.csv
  # 1983-12-30 -> 2011-01-16
 
  # http://ichart.finance.yahoo.com/table.csv?s=JPM &a=05 &b=1 &c=1983 &d=06 &e=1 &f=2011 &g=d &ignore=.csv
  # 1983-06-01 -> 2011-07-01
 
  encoded = urllib.urlencode(q) 
  
  url = URL_STEM + encoded # + "&ignore=.csv"
  print(url)
  return url 

def get_body(url):
  f = urllib.urlopen(url)
  body = f.read()
  f.close()
  return body

def get_csv_lines_for_period(symbol, fromY, fromM, fromD, toY, toM, toD):
  url = construct_ichart_csv_url(symbol, fromY, fromM, fromD, toY, toM, toD)
  body = get_body(url)
  return body






