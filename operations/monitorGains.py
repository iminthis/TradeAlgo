import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from getData.brokerfunc import get_positions, sell_stock_normal
import json, time, schedule


def checkgain():
    positions = get_positions()
    try:
        positions = positions['securitiesAccount']['positions']
    except:
        checkgain()
    for i in positions:
        pl = i['currentDayProfitLossPercentage']
        if pl < 80.0 and i['instrument']['symbol'] != "HCMC" and i['instrument']['symbol'] != "CCIV_082021C50":
            sell_stock_normal(int((round(pl)/100) * i["longQuantity"]), i['instrument']['symbol'])


schedule.every(5).minutes.do(checkgain)
while True:
    schedule.run_pending()
    time.sleep(1)
