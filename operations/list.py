import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from getData.brokerfunc import get_quote, getFloat, getVolume
from bs4 import BeautifulSoup

url = "https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/"
siteinfo = requests.get(url)

i = 0
content = siteinfo.content
html = content
parsed_html = BeautifulSoup(html, features="lxml")

doneList = []
for link in parsed_html.find_all('a'):
    a = link.get('href')
    if "symbol" in str(a) and "-" in str(a):
        if i < 25:
            i += 1
        else:
            x = a.split("-")
            x = x[1].split("/")
            doneList.append(x[0])
            i += 1

stockList = []

for stock in doneList:
    try: #there are mischars in the stocks!
        quote = get_quote(stock)
        if quote[stock]['lastPrice'] < 5.00 and quote[stock]['netChange'] >= 0.1 and quote[stock]['openPrice'] < quote[stock]['lastPrice'] and getVolume(stock) > 5000000 and float(getFloat(stock)) < 50000000.0:
            stockList.append(stock)
    except Exception as e:
        print(e)
        pass

print(stockList)