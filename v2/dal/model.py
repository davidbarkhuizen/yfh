from collections import namedtuple

Credential = namedtuple('Credential', ['host', 'database', 'user', 'password'])

DataSource = namedtuple('DataSource', ['Id', 'Name'])

Symbol = namedtuple('Symbol', ['Id', 'Code', 'Description'])
DailyPrice = namedtuple('DailyPrice', ['Id', 'Date', 'Open', 'High', 'Low', 'Close'])