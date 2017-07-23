from urllib.request import Request, urlopen
import re
import datetime
from collections import namedtuple
import calendar

# --------------------------------------------------------------------------------
# type definitions

YahooCredentials = namedtuple('YahooCredentials', ['Cookie', 'Crumb'])
HttpResponseData = namedtuple('HttpResponse', ['Info', 'Text'])

# --------------------------------------------------------------------------------

def write_to_file(file_path, text):

    with open(file_path, 'a') as out:
        out.write(text)
 
def get_regex_first_match(regex, text):

    match = re.search(regex, text)
    return match.group(1)

# --------------------------------------------------------------------------------

def http_get(url, cookie = None):
     
    headers = {'Cookie': cookie} if cookie else None
    request = Request(url)

    if cookie:
        request.add_header('Cookie', cookie)

    print(url)
    print(cookie)

    info, text = None, None

    try:

        with urlopen(request) as response:
            info = str(response.info())   
            text = str(response.read())

    # urllib.error.HTTPError: HTTP Error 401: Unauthorized
    except urllib.error.HTTPError as httpE: 

        print(httpE.code)
        print('code')
        print(type(httpE.code))
        print('reason')
        print(type(httpE.code))

        # HTTP Error 401: Unauthorized

    except Exception as e:
        print(e)
        raise e

    write_to_file('info.txt', info)
    write_to_file('text.txt', text)

    return HttpResponseData(Info = info, Text = text)

# --------------------------------------------------------------------------------
 
def get_yahoo_credentials(symbol):

    url = 'https://finance.yahoo.com/quote/{0}/history?p={0}'.format(symbol)

    response_data = http_get(url)

    # Set-Cookie: B=3u3f1b9cn3i60&b=3&s=c5; expires=Fri, 21-Jul-2018 09:26:24 GMT; path=/; domain=.yahoo.com
    #
    cookie_regex = r'Set-Cookie: (.*?);'
    cookie = get_regex_first_match(cookie_regex, response_data.Info)

    # "CrumbStore":{"crumb":"yg.r9.0LvYF"}
    #
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'   
    crumb = get_regex_first_match(crumble_regex, response_data.Text)

    return YahooCredentials(Cookie = cookie, Crumb = crumb)

# --------------------------------------------------------------------------------

def get_historial_data(credentials, symbol, date_from, date_to):

    time_stamp_from = calendar.timegm(datetime.datetime.strptime(date_from, "%Y-%m-%d").timetuple())
    time_stamp_to = calendar.timegm(datetime.datetime.strptime(date_to, "%Y-%m-%d").timetuple())

    quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}'

    url = quote_link.format(symbol, time_stamp_from, time_stamp_to, credentials.Crumb)

    return http_get(url, cookie=credentials.Cookie)

# --------------------------------------------------------------------------------

symbol = 'AAPL'

creds = get_yahoo_credentials(symbol)
print(creds)

data = get_historial_data(creds, symbol, '2010-01-01', '2017-07-21')
write_to_file('{0}.csv'.format(symbol), data.Text)