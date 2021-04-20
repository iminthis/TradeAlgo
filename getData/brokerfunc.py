import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
import yfinance as yf
from secret.config import key, account_number
from getData.getToken import getaccess

def get_price_history(symbol):
    symbol = str(symbol)
    url = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory"

    payload = {
        'apikey': key,
        'periodType': 'day',
        'frequencyType': 'minute',
        'frequency': '1',
        'period': '1'
    }

    history = requests.get(url, params=payload).json()

    return history

#print(json.dumps(get_price_history("PFMT"), indent = 4))


def get_quote(symbol):
    symbol = str(symbol)
    url = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes"

    payload = {
        'apikey': key,
    }

    quote = requests.get(url, params=payload).json()

    return quote

#print(json.dumps(get_quote("SPCB"), indent = 4))
#a = get_quote("MOTS")
#print(a["MOTS"]["lastPrice"])

def get_quotes():
    url = f"https://api.tdameritrade.com/v1/marketdata/quotes"

    payload = {
        'apikey': key,
        'symbol': 'HOTH,SGRP,PED,TGC,CHEK,HSTO,OEG,NTN,RCON,AVGR,ASRT,DVD'
    }

    quotes = requests.get(url, params=payload).json()

    return quotes

#print(json.dumps(get_quotes(), indent = 4))

'''
def get_access_token():
    url = "https://api.tdameritrade.com/v1/oauth2/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'grant_type': 'authorization_code',
        'access_type': 'offline',
        'code': parse_url,
        'client_id': key,
        'redirect_uri': 'http://localhost'
    }

    authreply = requests.post(url, headers = headers, data = payload).json()

    return authreply

print(get_access_token())
'''

def get_total_balance():
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
    bearer_key = "Bearer " + access_token
    url = "https://api.tdameritrade.com/v1/accounts"

    headers = {
        'Authorization': bearer_key
    }

    balance = requests.get(url, headers = headers).json()

    return balance

#account_stats = get_total_balance()
#print("Account Value: $" + str(account_stats[0]['securitiesAccount']['currentBalances']['liquidationValue']))

def get_cash_balance():
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
    bearer_key = "Bearer " + access_token
    url = "https://api.tdameritrade.com/v1/accounts"

    headers = {
        'Authorization': bearer_key
    }

    balance = requests.get(url, headers = headers).json()

    return balance

#account_stats = get_cash_balance()
#print(json.dumps(account_stats, indent=4))
#print("Amount Ready To Trade: $" + str(account_stats[0]['securitiesAccount']['projectedBalances']['cashAvailableForTrading']))

def get_positions():
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}"

    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()

    bearer_key = "Bearer " + access_token

    payload = {
        'fields': 'positions'
    }

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    send_order = requests.get(url, params=payload, headers=headers)

    if send_order.status_code == 401 or send_order.status_code == 403:
        getaccess()
        get_positions()

    return send_order.json()

#print(json.dumps(get_positions(), indent = 4))

def buy_stock(number_to_buy, symbol):
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
    #try:
    #    from getData.getToken import access_token
    #except:
    #    from getData.getToken import access_token

    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/orders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': 'BUY',
                'quantity': number_to_buy,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200 or send_order.status_code == 201:
        print("Order Placed!")
    else:
        print("Order Failed!")

'''def get_option_chain(symbol, contractType, strike, range, toExpire, optionType):
    try:
        from getData.getToken import access_token
    except:
        from getData.getToken import access_token

    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = "https://api.tdameritrade.com/v1/marketdata/chains"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        "apikey": key,
        "symbol": symbol,
        "contractType": contractType,
        "strike": strike,
        "range": range,
        "daysToExpiration": toExpire,
        "optionType": optionType
    }

    get_chain = requests.get(url, json = payload, headers = headers)
    get_chain_json = get_chain.json()

    return get_chain_json, get_chain.status_code

print(json.dumps(get_option_chain("AAPL", "PUT", "124", "OTM", "5", "S"), indent = 4))'''

#get_option_chain("AAPL", "PUT", "124", "OTM", "5", "S")

'''def trail_stock(number_to_sell, symbol):
    from getToken import access_token
    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/orders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        "complexOrderStrategyType": "NONE",
        "orderType": "TRAILING_STOP",
        "session": "NORMAL",
        "stopPriceLinkBasis": "BID",
        "stopPriceLinkType": "VALUE",
        "stopPriceOffset": 0.10,
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': 'SELL',
                'quantity': number_to_sell,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200:
        print("Order Placed!")
    else:
        print("Order Failed!")

trail_stock("ASRT", 16)
'''

def sell_stock(number_to_sell, symbol):
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
        
    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/orders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        "complexOrderStrategyType": "NONE",
        'orderType': 'TRAILING_STOP',
        'session': 'NORMAL',
        "stopPriceLinkBasis": "BID",
        "stopPriceLinkType": "PERCENT",
        "stopPriceOffset": 15,
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': 'SELL',
                'quantity': number_to_sell,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200 or send_order.status_code == 201:
        print("Order Placed!")
    else:
        print("Order Failed!")

#sell_stock(13, "AVGR")

def sell_stock_normal(number_to_sell, symbol):
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/orders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': 'SELL',
                'quantity': number_to_sell,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200 or send_order.status_code == 201:
        print("Order Placed!")
    else:
        print(send_order.content)



def place_saved_order(number_to_buy, symbol, typeof):
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
    symbol = str(symbol)
    typeof = str(typeof)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/savedorders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': typeof,
                'quantity': number_to_buy,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200 or send_order.status_code == 201:
        print("Order Placed!")
    else:
        print("Order Failed!")

#place_saved_order(1, "AAPL", "Buy")

def query_saved_order():
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/savedorders"

    headers = {
        'Authorization': bearer_key,
    }

    send_query = requests.get(url, headers = headers).json()

    return send_query

#print(json.dump(query_saved_order(), indent = 4))
def get_share_balance():
    #getaccess()
    f = open("access_token.txt", "r")
    access_token = f.readline()
    f.close()
    bearer_key = "Bearer " + access_token
    url = "https://api.tdameritrade.com/v1/accounts"

    payload = {
        'fields': "positions"
    }

    headers = {
        'Authorization': bearer_key
    }

    balance = requests.get(url, params = payload, headers = headers).json()

    return balance

def getFloat(symbol):
    url = "https://www.marketwatch.com/investing/stock"

    updatedurl = f"{url}/{symbol}?mod=quote_search"
    quote = requests.get(updatedurl)
    soup = BeautifulSoup(quote.content, 'html.parser')
    list_tags = soup.find_all(class_="primary")
    final = str(list_tags[21])
    final = final.split('<span class="primary">')
    final = final[1].split("</span>")
    final = final[0]
    if "M" in final:
        final = final.split("M")
        final = final[0]
        final = float(final) * 10**6
        final = str(final)
    elif "B" in final:
        final = final.split("B")
        final = final[0]
        final = float(final) * 10**9
        final = str(final)
    elif "K" in final:
        final = final.split("K")
        final = final[0]
        final = float(final) * 10**3
        final = str(final)

    return final

#print(getFloat("SPCB"))

def getVolume(symbol):
    key = "ce4e7efb80a707ca2b1edcec4ed54ffd"
    url = "https://financialmodelingprep.com"
    endpoint = f"{url}/api/v3/quote/{symbol}?apikey={key}"

    data = requests.get(endpoint).json()

    return data[0]['volume']

#print(json.dumps(getVolume("SPCB"), indent = 4))

def get15(symbol):

    data = yf.download(tickers=symbol, period="1d", interval = "15m")

    return data.tail()


#print(get15("CCIV"))

'''stock_stats = get_share_balance()
print(json.dumps(stock_stats, indent = 4))

i = 0
for stock in stock_stats[0]['securitiesAccount']['positions']:
    stock_sym = str(stock_stats[0]['securitiesAccount']['positions'][i]['instrument']['symbol'])
    num_to_sell = str(stock_stats[0]['securitiesAccount']['positions'][i]['longQuantity'])
    quote = get_quote(stock_sym)
    getQuote = get_quote(stock_sym)
    currentPrice = getQuote[stock_sym]['lastPrice']
    sell_stock(num_to_sell, stock_sym, currentPrice - 0.10)
    print(stock_sym + " sold!")
    i += 1'''
