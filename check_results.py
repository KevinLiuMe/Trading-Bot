import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol, start_time, end_time):
    data = yf.download(symbol, start=start_time, end=end_time, interval="1d")
    if data.empty:
        print(f"No data available for symbol {symbol} between {start_time} and {end_time}.")
        return None
    data.index = pd.to_datetime(data.index)
    return data

def fetch_and_print_stock_data(symbol, start_time, end_time):
    data = fetch_stock_data(symbol, start_time, end_time)
    if data is not None:
        print(f"\nStock: {symbol}")
        print(f"\nAvailable Data from {start_time} to {end_time}:")
        print(data)
    return data

def fetch_data(symbol, start_time, end_time):
    data = yf.download(symbol, start=start_time, end=end_time, interval="1d")
    
    if data.empty:
        print(f"No data available for symbol {symbol} between {start_time} and {end_time}.")
        return None

    data.index = pd.to_datetime(data.index)
    return data

def find_nearest_date(df, target_date):
    nearest_date = min(df.index, key=lambda d: abs(d - target_date))
    return nearest_date

def fetch_and_print_stock_data(symbol, start_time, end_time):
    data = fetch_data(symbol, start_time, end_time)
    
    if data is None:
        return None, None

    start_timestamp = pd.Timestamp(start_time)
    end_timestamp = pd.Timestamp(end_time)
    
    data_within_range = data.loc[start_timestamp:end_timestamp]
    
    if data_within_range.empty:
        start_date = find_nearest_date(data, start_timestamp)
        end_date = find_nearest_date(data, end_timestamp)
        
        data_within_range = data.loc[start_date:end_date]
        
        print(f"\nExact data not available. Showing data for nearest available dates:")
        print(f"Data on Nearest Start Date: {start_date}")
        print(f"Data on Nearest End Date: {end_date}")
    
    return data_within_range

def main():
    symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
    start_time = input("Enter the start time (YYYY-MM-DD): ")
    end_time = input("Enter the end time (YYYY-MM-DD): ")

    data_within_range = fetch_and_print_stock_data(symbol, start_time, end_time)
    
    if data_within_range is not None:
        print(f"\nStock: {symbol}")
        print(f"\nAvailable Data from {start_time} to {end_time}:")
        print(data_within_range)

if __name__ == "__main__":
    main()


