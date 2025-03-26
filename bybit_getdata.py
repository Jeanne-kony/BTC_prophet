from datetime import datetime
import time

import requests
import pandas as pd
from tqdm import tqdm

url = "https://api.bybit.com/v5/market/kline"
symbol = "BTCUSDT"
# spot,linear,inverse
category = "linear"
# 1,3,5,15,30,60,120,240,360,720,D,M,W
interval = 15

timestamp = int(time.time())
values = []
# 初回リクエストで総データ数を推定
initial_params = {
    "symbol": symbol,
    "interval": interval,
    "category": category,
    "start": (timestamp - 200 * 60 * interval) * 1000,
    "end": timestamp * 1000,
    "limit": 200
}
initial_response = requests.get(url, params=initial_params)
initial_data = initial_response.json()
estimated_total = len(initial_data["result"]["list"])
values += initial_data["result"]["list"]
timestamp = int(time.time())
values = []

# tqdmでプログレスバーを表示
with tqdm(total=estimated_total, desc="データ取得中") as pbar:
    pbar.update(len(initial_data["result"]["list"]))
    
    while True:
        params = {
            "symbol": symbol,
            "interval": interval,
            "category": category,
            "start": (timestamp - 200 * 60 * interval) * 1000,
            "end": timestamp * 1000,
            "limit": 200
        }

        response = requests.get(url, params=params)
        response_data = response.json()
        
        if len(response_data["result"]["list"]) == 0:
            break

        new_data = response_data["result"]["list"]
        values += new_data
        timestamp -= 200 * 60 * interval
        
        # プログレスバーを更新
        pbar.update(len(new_data))
        # 必要に応じて総数を調整
        if pbar.total < len(values):
            pbar.total = len(values) + estimated_total

data = pd.DataFrame(values)
data.to_csv(f"bybit_{symbol}_{category}_{interval}.csv", index=False)
