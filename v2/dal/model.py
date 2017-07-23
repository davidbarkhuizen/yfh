from collections import namedtuple

Symbol = namedtuple('Symbol', ['Id', 'Code', 'Description'])
DailyPrice = namedtuple('DailyPrice', ['Id', 'Date', 'Open', 'High', 'Low', 'Close'])