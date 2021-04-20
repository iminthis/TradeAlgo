import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from getData.brokerfunc import get_share_balance, sell_stock_normal


#from stocklist import stockList, realStockAmt
def sell():
    stock_stats = get_share_balance()
    #print(json.dumps(stock_stats, indent = 4))

    i = 0
    for stock in stock_stats[0]['securitiesAccount']['positions']:
        stock_sym = str(stock_stats[0]['securitiesAccount']['positions'][i]['instrument']['symbol'])
        num_to_sell = str(stock_stats[0]['securitiesAccount']['positions'][i]['longQuantity'])
        #print(stock_sym)
        #print(num_to_sell)
        sell_stock_normal(num_to_sell, stock_sym)
        print(stock_sym + " sold!")
        i += 1

#schedule.every().day.at("12:59").do(sell)

#while True:
#    schedule.run_pending()
#    time.sleep(1)

