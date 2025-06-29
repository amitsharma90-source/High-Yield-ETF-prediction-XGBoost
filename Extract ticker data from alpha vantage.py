# -*- coding: utf-8 -*-
"""
Created on Sat Jun  7 18:15:43 2025

@author: amits
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 26 20:26:20 2025

@author: amits
"""

import pandas as pd
import requests
import time
from datetime import datetime
import pandas_datareader.data as web

# ==========================================
# Option 1: Alpha Vantage (Full History)
# ==========================================
# def download_alpha_vantage_full_history(tickers, api_key, start_date="2010-01-01"):
"""
Alpha Vantage provides FULL historical data (20+ years)
Limitation: Only 25 calls per day on free tier
Get free key: https://www.alphavantage.co/support/#api-key
"""
print("📥 Using Alpha Vantage for full historical data...")
all_data = {}
# tickers = ['IWF', 'IWD', 'MGK', 'MGV', 'XLY','XLP', 'XLU']
tickers = ['LQD', 'TLT', 'SHY']
# start_date = datetime.datetime(2010, 1, 1)
start_date = "1970-01-01"
for i, ticker in enumerate(tickers):
    print(f"Downloading {ticker} ({i+1}/{len(tickers)}) - Full history since IPO")
    
    try:
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'apikey': 'XXXXXXXX',
            'outputsize': 'full'  # This gets ALL available data
        }
        
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        if 'Time Series (Daily)' in data:
            df = pd.DataFrame(data['Time Series (Daily)']).T
            df.index = pd.to_datetime(df.index)
            df = df.astype({'4. close': float}).sort_index()
            
            # Filter by start date
            df = df[df.index >= start_date]
            all_data[ticker] = df['4. close']
            
            print(f"  ✅ {ticker}: {len(df)} records from {df.index.min().date()} to {df.index.max().date()}")
            
        elif 'Error Message' in data:
            print(f"  ❌ {ticker}: {data['Error Message']}")
        elif 'Note' in data:
            print(f"  ⚠️ Rate limit hit. Free tier allows 25 calls/day")
            break
        else:
            print(f"  ❌ {ticker}: Unexpected response")
            
    except Exception as e:
        print(f"  ❌ {ticker}: {e}")
    
    # Rate limiting: 5 calls per minute for free tier
    if i < len(tickers) - 1:
        print("  ⏳ Waiting 12 seconds (rate limit)...")
        time.sleep(12)

# return pd.DataFrame(all_data)
# all_data.to_csv("all_ticker_data.csv")
# Convert dictionary of series to DataFrame, then save:
combined_df = pd.DataFrame(all_data)
combined_df.to_csv("Extra Ticker, Growth, Value, Small, Large, ctclical.csv", index=True)

# all_data = download_alpha_vantage_full_history('macro_data.csv', download_macro_data)
