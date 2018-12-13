import requests
from datetime import datetime
import time
import ccxt


bitflyer = ccxt.bitflyer()
bitflyer.apiKey = ''
bitflyer.secret = ''


# Cryptowatchから価格を取得する関数
def get_price(min):
    # APIで価格を取得する
    response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc", params={"periods": min})
    data = response.json()
    last_data = data["result"][str(min)][-2]

    return { "close_time" : last_data[0],
             "open_price" : last_data[1],
             "high_price" : last_data[2],
             "low_price" : last_data[3],
             "close_price" : last_data[4]
    }


# 日時・終値・始値を表示する関数を作成する。
def print_price( data ) :
    print("時間 : " + datetime.fromtimestamp(data[ "close_time" ]).strftime('%Y/%m/%d %H:%M')
          + " 始値 : " + str(data["open_price"])
          + " 終値 : " + str(data["close_price"])
          )

def check_candle( data ) :
    real_body_rate = abs(data["close_price"] - data["open_price"]) / (data["high_price"] - data["low_price"])
    increase_rate = data["close_price"] / data["open_price"] - 1

    if data["close_price"] < data["open_price"] : return False
    elif increase_rate < 0.0005 : return False
    elif real_body_rate < 0.5 : return False
    else: return True

def check_ascend( data, last_data ) :
    if data["open_price"] > last_data["open_price"] and data["close_price"] > last_data["close_price"] :
        return True
    else:
        return False

last_data = get_price(60)
print_price( last_data )
flag = 0

while True:
    # get_price()関数を使って最新のローソク足の日時・始値：終値を取得する
    data = get_price(60)

    if data["close_time"] != last_data["close_time"] :
        print_price( data )

        if flag == 0 and check_candle( data ) :
            flag = 1
        elif flag == 1 and check_candle( data ) and check_ascend(data, last_data) :
            print("2本連続で陽線")
            flag = 2
        elif flag == 2 and check_candle( data ) and check_ascend(data, last_data) :
            print("3本連続で陽線なので買い！")
            flag = 3
        else:
            flag = 0

        last_data["close_time"] = data["close_time"]
        last_data["open_price"] = data["open_price"]
        last_data["close_price"] = data["close_price"]

    time.sleep(10)
