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
    # Calculate True Range
    data['Prev_Close'] = data['Close'].shift(1)
    data['TR'] = data[['High', 'Low', 'Prev_Close']].apply(
        lambda x: max(x['High'] - x['Low'], abs(x['High'] - x['Prev_Close']), abs(x['Low'] - x['Prev_Close'])),
        axis=1
    )
    
    # Calculate ATR
    data['ATR'] = data['TR'].rolling(window=atr_window).mean()
    
    # Replace NaN values in ATR with the average ATR over the time frame
    atr_mean = data['ATR'].mean()
    data['ATR'].fillna(atr_mean, inplace=True)
    
    # Drop intermediate columns
    data.drop(columns=['Prev_Close', 'TR'], inplace=True)
    
    return data

# Function to manually mark breakout times
def mark_breakouts(data, breakout_times):
    # Initialize the is_breakout column with 0
    data['is_breakout'] = 0

    # Convert breakout_times to datetime format with timezone info
    timezone = data.index.tz  # Get the timezone of the DataFrame index
    breakout_times = [pd.to_datetime(time).tz_localize(timezone) for time in breakout_times]

    # Mark the specified breakout times with 1
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
            # Parse the input and check for validity
            parsed_time = parser.parse(user_input)
            breakout_times.append(parsed_time)
        except ValueError:
            print("Invalid format. Please enter the date and time in the format YYYY-MM-DD HH:MM:SS.")

    return breakout_times

# Interactive Inputs
symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Convert start_date to datetime
start_date_dt = pd.to_datetime(start_date)

# Calculate the earliest date needed for calculations (20 days before start_date)
earliest_date = start_date_dt - timedelta(days=20)

# Fetch hourly historical data from Yahoo Finance starting from the earliest date
hourly_data = yf.download(symbol, start=earliest_date, end=end_date, interval="1h")

# Calculate RSI and add it as a new column to the DataFrame
hourly_data['RSI'] = calculate_rsi(hourly_data)

# Calculate CIV and add it as a new column to the DataFrame
hourly_data = calculate_civ(hourly_data)

# Calculate Deviation from SMA and add it as a new column to the DataFrame
hourly_data = calculate_deviation_from_sma(hourly_data)

# Calculate ATR and add it as a new column to the DataFrame
hourly_data = calculate_atr(hourly_data)

# User inputs the breakout times
breakout_times = input_breakout_times()

# Apply the function to mark the breakouts
hourly_data = mark_breakouts(hourly_data, breakout_times)

# Select only the required columns for the output
final_columns = ['Open', 'Close', 'RSI', 'CIV', 'SMA', 'ATR', 'is_breakout']
hourly_data = hourly_data[final_columns]

# Define path to the desktop and the output file
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, f"{symbol}_result.csv")

# Export results to a CSV file on the desktop with the stock symbol as the filename
hourly_data.to_csv(output_file, index=True)

# Output the results
print(f"\nResults exported to {output_file}.")




