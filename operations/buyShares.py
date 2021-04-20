import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import requests
from bs4 import BeautifulSoup
from getData.brokerfunc import get_quote, get_cash_balance, buy_stock, sell_stock, getFloat, getVolume
from getData.getToken import getaccess
import schedule
    
print("\x1b[8;50;115t")

print('''
 $$$$$$\              $$\                $$$$$$\    $$\                         $$\       
$$  __$$\             $$ |              $$  __$$\   $$ |                        $$ |      
$$ /  $$ |$$\   $$\ $$$$$$\    $$$$$$\  $$ /  \__|$$$$$$\    $$$$$$\   $$$$$$$\ $$ |  $$\ 
$$$$$$$$ |$$ |  $$ |\_$$  _|  $$  __$$\ \$$$$$$\  \_$$  _|  $$  __$$\ $$  _____|$$ | $$  |
$$  __$$ |$$ |  $$ |  $$ |    $$ /  $$ | \____$$\   $$ |    $$ /  $$ |$$ /      $$$$$$  / 
$$ |  $$ |$$ |  $$ |  $$ |$$\ $$ |  $$ |$$\   $$ |  $$ |$$\ $$ |  $$ |$$ |      $$  _$$<  
$$ |  $$ |\$$$$$$  |  \$$$$  |\$$$$$$  |\$$$$$$  |  \$$$$  |\$$$$$$  |\$$$$$$$\ $$ | \$$\ 
\__|  \__| \______/    \____/  \______/  \______/    \____/  \______/  \_______|\__|  \__|
'''
)

STARTTIME = "07:14"
TOKENTIME = "07:05"
print(f"EXECUTING @ {STARTTIME}")

def buy():
    print("Starting...")
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
        except:
            pass

    length = len(stockList)
    balance = get_cash_balance()
    stockDiv = balance[0]['securitiesAccount']['projectedBalances']['cashAvailableForTrading'] / float(length)

    for stocky in stockList:
        quote1 = get_quote(stocky)
        stockCount = stockDiv / quote1[str(stocky)]['lastPrice']
        realStockAmt = round(stockCount)
        buy_stock(realStockAmt, stocky)
        print("Order Placed For: " + str(stocky) + " Number of Shares Bought: " + str(realStockAmt))
        sell_stock(realStockAmt, stocky)
        print("Order Placed For: " + str(stocky) + " Number of Shares Trailed: " + str(realStockAmt))

    print("----------------------------------------------------------------------------------\nProgram Finished!")


#getaccess()
#buy()


schedule.every().day.at(TOKENTIME).do(getaccess)
schedule.every().day.at(STARTTIME).do(buy)

while True:
    schedule.run_pending()
    time.sleep(1)