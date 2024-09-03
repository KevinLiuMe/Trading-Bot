import os
import yfinance as yf
import pandas as pd
from dateutil import parser
import pytz
from datetime import timedelta
# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate CIV (Change in Volume)
def calculate_civ(data):
    avg_volume = data['Volume'].mean()
    data['CIV'] = ((data['Volume'] - avg_volume) / avg_volume) * 100
    return data

# Function to calculate deviations from the 20-day SMA
def calculate_deviation_from_sma(data, sma_window=20):
    data['SMA_20'] = data['Close'].rolling(window=sma_window).mean()
    data['STD_20'] = data['Close'].rolling(window=sma_window).std()
    data['SMA'] = (data['Close'] - data['SMA_20']) / data['STD_20']
    return data

# Function to calculate the Average True Range (ATR)
def calculate_atr(data, atr_window=2):
    data['Prev_Close'] = data['Close'].shift(1)
    data['TR'] = data[['High', 'Low', 'Prev_Close']].apply(
        lambda x: max(x['High'] - x['Low'], abs(x['High'] - x['Prev_Close']), abs(x['Low'] - x['Prev_Close'])),
        axis=1
    )
    
    data['ATR'] = data['TR'].rolling(window=atr_window).mean()

    atr_mean = data['ATR'].mean()
    data['ATR'].fillna(atr_mean, inplace=True)

    data.drop(columns=['Prev_Close', 'TR'], inplace=True)
    
    return data

# Function to manually mark breakout times
def mark_breakouts(data, breakout_times):
    data['is_breakout'] = 0

    timezone = data.index.tz  # Get the timezone of the DataFrame index
    breakout_times = [pd.to_datetime(time).tz_localize(timezone) for time in breakout_times]

 
    for time in breakout_times:
        if time in data.index:
            data.at[time, 'is_breakout'] = 1
        else:
            print(f"Breakout time not found in DataFrame index: {time}")

    return data

# Function to input breakout times
def input_breakout_times():
    breakout_times = []
    print("Enter the breakout times (format: YYYY-MM-DD HH:MM:SS). Enter 'done' to finish.")
    while True:
        user_input = input("Enter a breakout time: ")
        if user_input.lower() == 'done':
            break
        try:
            parsed_time = parser.parse(user_input)
            breakout_times.append(parsed_time)
        except ValueError:
            print("Invalid format. Please enter the date and time in the format YYYY-MM-DD HH:MM:SS.")

    return breakout_times

# Inputs
symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

start_date_dt = pd.to_datetime(start_date)

earliest_date = start_date_dt - timedelta(days=20)

hourly_data = yf.download(symbol, start=earliest_date, end=end_date, interval="1h")

hourly_data['RSI'] = calculate_rsi(hourly_data)

hourly_data = calculate_civ(hourly_data)

hourly_data = calculate_deviation_from_sma(hourly_data)

hourly_data = calculate_atr(hourly_data)

breakout_times = input_breakout_times()

hourly_data = mark_breakouts(hourly_data, breakout_times)

final_columns = ['Open', 'Close', 'RSI', 'CIV', 'SMA', 'ATR', 'is_breakout']
hourly_data = hourly_data[final_columns]

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, f"{symbol}_result.csv")

hourly_data.to_csv(output_file, index=True)

print(f"\nResults exported to {output_file}.")




