import requests
import time
import pandas as pd

# WazirX API base URL
base_url = "https://api.wazirx.com/api/v1"

# Symbols to analyze
symbols = ["btcusdt", "ethusdt"]

# Function to get historical klines (candlestick data) for a symbol
def get_klines(symbol, interval, limit=100):
    url = f"{base_url}/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

# Function to calculate moving averages
def calculate_moving_averages(df, short_period, long_period):
    df["SMA_Short"] = df["close"].rolling(window=short_period).mean()
    df["SMA_Long"] = df["close"].rolling(window=long_period).mean()

# Function to write buy/sell signals to a text file
def write_signals(symbol, signal):
    with open("signals.txt", "a") as file:
        file.write(f"{symbol}: {signal}\n")

# Swing trading parameters
short_ma_period = 50
long_ma_period = 200

while True:
    for symbol in symbols:
        klines = get_klines(symbol, "1d", 300)  # Fetch 300 days of daily data
        calculate_moving_averages(klines, short_ma_period, long_ma_period)
        
        if klines["SMA_Short"].iloc[-1] > klines["SMA_Long"].iloc[-1] and klines["SMA_Short"].iloc[-2] <= klines["SMA_Long"].iloc[-2]:
            write_signals(symbol, "Buy")
        elif klines["SMA_Short"].iloc[-1] < klines["SMA_Long"].iloc[-1] and klines["SMA_Short"].iloc[-2] >= klines["SMA_Long"].iloc[-2]:
            write_signals(symbol, "Sell")
    
    time.sleep(86400)  # Sleep for one day (adjust the interval as needed)

# This script uses a simple crossover strategy with daily data. Adjust parameters and criteria as needed for your specific strategy.
