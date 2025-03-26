import requests
import os
import sys
import requests
import json
import time
from datetime import datetime
import pandas as pd
from dateutil import tz
def get_funding_rate_history(symbol, end_time):
    endPoint = 'https://api.bybit.com'
    path     = '/v5/market/funding/history'
    url = endPoint + path

    params = {
        'category': 'linear',
        'symbol': symbol,
        'endTime': end_time,
    }

    response = requests.get(url, params=params)
    res = response.json()
    return res

def convert_data(data):
    # FRデータを入れるDataFrame。
    df = pd.DataFrame()
    # FRデータが入っているリストから情報を取り出して、DataFrameに入れる。
    for d in data['result']['list']:
        df_add = pd.DataFrame(d, index=[0])
        df = pd.concat([df, df_add], axis='index')
    df = df.reset_index(drop=True)
    # FRはfloat型に変換する。
    df['fundingRate'] = df['fundingRate'].astype('float64')
    # タイムスタンプはint型に変換する。
    df['fundingRateTimestamp'] = df['fundingRateTimestamp'].astype('int64')
    return df


JST = tz.gettz('Asia/Tokyo')
UTC = tz.gettz('UTC')
# 現在のUTC時刻を取得しておく。
now_utc = datetime.now(UTC)
# 取得するFRの通貨ペアを設定する。
# 今回はBTCUSDTとする。
symbol = 'BTCUSDT'
# エンドタイムスタンプを初期化する。
end_time = None
# FRを入れるDataFrameを初期化する。
df_fr = pd.DataFrame()
# ここから、ループ文で3ヶ月分のFRを取得する。
while True:
    # FRを取得する
    # end_timeはwhile文の中で毎回更新される。
    data = get_funding_rate_history(symbol, end_time)
    # 取得したFRを日付をIndexとするDataFrameに変換する。
    df_add = convert_data(data)
    # FRを保存するDataFrameに追加する。
    df_fr = pd.concat([df_fr, df_add], axis='index')
    # タイムスタンプのUNIX時間でソートする。未来の時刻が下側になるようにソートする。
    df_fr = df_fr.sort_values(by=['fundingRateTimestamp'], ascending=True)
    # 重複行は先頭を残す。
    # タイムスタンプで重複を判断する。
    df_fr = df_fr.drop_duplicates(subset='fundingRateTimestamp', keep='first')
    # Indexの通し番号を再度付与する。
    df_fr = df_fr.reset_index(drop=True)
    # 取得済みのFRの最も古いタイムスタンプを取得し、次に取得するFRの最後のタイムスタンプとする。
    # 先頭が最も古いタイムスタンプとなる。
    end_time = df_fr.iat[0, df_fr.columns.get_loc('fundingRateTimestamp')]
    # 最も古いタイムスタンプをUTC時刻に変換する。
    end_time_utc = datetime.fromtimestamp(end_time/1000, UTC)
 
    if (now_utc - end_time_utc).days > 31 * 24:
        break
    # 短時間にAPIを何度も呼ばないように1秒間寝る。
    time.sleep(1)
# FR情報をファイル出力する。
filename = 'df_fr.csv'
file_path = os.path.join('/Users/estyle-155/Documents/cyptocurrency_python', filename)
df_fr.to_csv(file_path)