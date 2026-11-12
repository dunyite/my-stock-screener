import datetime
import json
import yfinance as yf

# 示範清單 (實務上可擴充為全台股上市櫃股票清單，並自動過濾金融與ETF)
stock_symbols = [
    "2330.TW",
    "2454.TW",
    "3231.TW",
    "2382.TW",
    "1513.TW",
    "1503.TW",
    "3017.TW",
    "3661.TW",
    "6669.TW",
    "2603.TW",
]

results = []

for symbol in stock_symbols:
  try:
    df = yf.download(symbol, period="3mo", progress=False)
    if len(df) < 60:
      continue

    # 處理 Pandas 欄位結構相容性
    close = df["Close"].squeeze()
    volume = df["Volume"].squeeze()

    ma1 = float(close.iloc[-1])
    ma60 = float(close.rolling(60).mean().iloc[-1])
    vol_today = float(volume.iloc[-1])
    vol_yest = float(volume.iloc[-2])
    close_1d_ago = float(close.iloc[-2])
    close_2d_ago = float(close.iloc[-3])
    turnover = vol_today * ma1  # 成交金額 (元)

    # 6大選股條件檢核
    cond1 = ma1 >= 50
    cond2 = close_1d_ago > (close_2d_ago * 1.09)
    cond3 = vol_today > vol_yest
    cond4 = turnover > 1000000000  # 大於10億元
    cond5 = ma1 > ma60
    cond6 = vol_today > 9999

    if all([cond1, cond2, cond3, cond4, cond5, cond6]):
      results.append({
          "symbol": symbol,
          "price": ma1,
          "volume": int(vol_today),
          "turnover": turnover / 100000000,  # 換算億元
          "ma60": ma60,
      })
  except Exception as e:
    print(f"Error {symbol}: {e}")

output_data = {
    "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    "count": len(results),
    "stocks": results,
}

with open("stocks_data.json", "w", encoding="utf-8") as f:
  json.dump(output_data, f, ensure_ascii=False, indent=4)
print(f"Successfully generated stocks_data.json with {len(results)} stocks.")