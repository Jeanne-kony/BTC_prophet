- BTCの終値を予測をするため以下の特徴量を使用した
- Federal Reserve Economic Data(https://fred.stlouisfed.org/) からNominal Broad U.S. Dollar Index
- bybit(https://www.bybit.com/ja-JP/) からBTCの過去レートと資金調達率
- Investing.com(https://jp.investing.com/indices/us-spx-500-historical-data) からS&P500の過去のレート

  上記の特徴量を追加することによって平均絶対パーセント誤差 (MAPE)を 5.20%　→ 5.18%に向上した
  
  特徴量を追加するにあたって、時間の粒度を合わせるための欠損値の補完は前埋め法を使用した
  
  予測モデルはprophetを使用した
  
  今回は時系列データを特徴量として使用したが、時系列で分けるのではなく取引量などにデータを整形すればデータがIID ガウス分布に近づく研究結果があるため次回はそのようにデータを加工する
