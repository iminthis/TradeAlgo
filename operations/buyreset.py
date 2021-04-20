#remake for reference

'''import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import requests
from bs4 import BeautifulSoup
from getData.brokerfunc import get_quote, get_cash_balance, buy_stock, sell_stock, getFloat, getVolume, get15
import schedule

def hello():
    print(getFloat("AAPL"))

print("\x1b[8;50;115t")

#ascii art here

STARTTIME = "07:14"
print(f"EXECUTING @ {STARTTIME}")

def buy():
    print("Starting...")
    url = "https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/"
    siteinfo = requests.get(url)

    i = 0
    content = siteinfo.content
    html = content
    parsed_html = BeautifulSoup(html, features="lxml")
    badlist = []
    goodlist = []
    for link in parsed_html.find_all('a'):
        a = link.get('href')
        if "symbol" in str(a) and "-" in str(a):
            if i < 25:
                badlist.append(a)
                i += 1
            else:
                goodlist.append(a)
                i += 1

    finallist = []
    doneList = []
    for z in goodlist:
        x = z.split("-")
        finallist.append(x[1])
    for item in finallist:
        y = item.split("/")
        doneList.append(y[0])
    #print(doneList)

    stockList = []

    for stock in doneList:
        try:
            quote = get_quote(stock)
            print(stock)
            print(value)
            print(change[stock]['netChange'])
            print(change[stock]['openPrice'])
            print(change[stock]['lastPrice'])
            print(getVolume(stock))
            print(getFloat(stock))
            print(getVolume(stock) > 1000000)
            print(float(getFloat(stock)) < 100000000.0)
            if quote[stock]['closePrice'] < 5.00 and quote[stock]['netChange'] >= 0.2 and quote[stock]['openPrice'] < quote[stock]['lastPrice'] and getVolume(stock) > 1000000 and float(getFloat(stock)) < 100000000.0:
                #print(stock + " success")
                stockList.append(stock)
        except:
            pass

    #print(stockList)

    length = len(stockList)
    balance = get_cash_balance()
    stockDiv = balance[0]['securitiesAccount']['projectedBalances']['cashAvailableForTrading'] / float(length)
    #balance = 392
    #stockDiv = balance / float(length)
    realStockAmt = []
    stockAmt = []
    #print(stockList)
    for stocky in stockList:
        quote1 = get_quote(stocky)
        #print(json.dumps(quote1, indent = 4))
        stockCount = stockDiv / quote1[str(stocky)]['lastPrice']
        stockAmt.append(stockCount)

    for thing in stockAmt:
        xy = round(thing)
        realStockAmt.append(xy)

    print(stockList)
    print(realStockAmt)
    print("Each stock gets: $" + str(stockDiv))

    monkeyCount = 0
    for monkey in stockList:
        buy_stock(realStockAmt[monkeyCount], stockList[monkeyCount])
        print("Order Placed For: " + str(stockList[monkeyCount]) + " Number of Shares Bought: " + str(realStockAmt[monkeyCount]))
        sell_stock(realStockAmt[monkeyCount], stockList[monkeyCount])
        print("Order Placed For: " + str(stockList[monkeyCount]) + " Number of Shares Trailed: " + str(realStockAmt[monkeyCount]))
        monkeyCount += 1

    print("----------------------------------------------------------------------------------\nProgram Finished!")

#buy()

schedule.every().day.at(STARTTIME).do(buy)

while True:
    schedule.run_pending()
    time.sleep(1)'''

#create validation function