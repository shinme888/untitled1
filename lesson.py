import ccxt
from pprint import pprint

bitflyer = ccxt.bitflyer()
bitflyer.apiKey = 'TR9eWhEgzWBS2tNDBBGCWN'
bitflyer.secret = 'DkKprwh+cGRqMAPMZn/FZQu31phWOd4SXHrw4M02iiw='

orders = bitflyer.fetch_open_orders(
    symbol = "BTC/JPY",  #通貨ペア
    params = {"product_code": "FX_BTC_JPY"}     #各取引所のAPIに渡せるパラメーター
)

for o in orders :
    bitflyer.cancel_order(
        symbol = "BTC/JPY",
        id = o["id"],
        params = {"product_code" : "FX_BTC_JPY"}
    )

'''
for o in orders:
    pprint(o["datetime"])
    pprint(o["id"])
    pprint(o["cost"])
    pprint(" ")


'''
'''
order = bitflyer.create_order(
	symbol = 'BTC/JPY',
	type='limit',
	side='buy',
	price='358000',
	amount='0.01',
	params = { "product_code" : "FX_BTC_JPY" })

pprint( order )
'''