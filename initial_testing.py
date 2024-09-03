import os
import yfinance as yf
import pandas as pd

symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
window = int(input("Enter the window size for resistance calculation (e.g., 20): "))

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, f"{symbol}.csv")

daily_data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
hourly_data = yf.download(symbol, start=start_date, end=end_date, interval="1h")

def identify_resistance(data, window=20):
    data['Resistance'] = data['High'].rolling(window=window).max()
    return data

daily_data = identify_resistance(daily_data, window)

def detect_breakouts(hourly_data, resistance_level):
    breakouts = hourly_data[hourly_data['Close'] > resistance_level]
    return breakouts
    
most_recent_resistance = daily_data['Resistance'].iloc[-1]

hourly_breakouts = detect_breakouts(hourly_data, most_recent_resistance)

def place_orders_and_backtest(breakouts, hourly_data):
    results = []
    for _, breakout in breakouts.iterrows():
        entry_time = breakout.name
        entry_price = breakout['Close']

        subsequent_candles = hourly_data.loc[hourly_data.index > entry_time]
        if not subsequent_candles.empty:
            subsequent_candle = subsequent_candles.iloc[0]
            exit_price = subsequent_candle['Close']
            profit = exit_price - entry_price
            
            result = {
                'entry_time': entry_time,
                'entry_price': entry_price,
                'exit_time': subsequent_candle.name,
                'exit_price': exit_price,
                'profit': profit
            }
            results.append(result)

    return results

backtest_results = place_orders_and_backtest(hourly_breakouts, hourly_data)

results_df = pd.DataFrame(backtest_results)

if not results_df.empty:
    total_profit = results_df['profit'].sum()
    initial_investment = len(results_df) * results_df['entry_price'].mean() 
    overall_profit_margin = (total_profit / initial_investment) * 100 if initial_investment > 0 else 0
else:
    total_profit = 0
    overall_profit_margin = 0

results_df.to_csv(output_file, index=False)

print(f"\nResults exported to {output_file}.")
print(f"Overall Profit Margin: {overall_profit_margin:.2f}%")

symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
window = int(input("Enter the window size for resistance calculation (e.g., 20): "))

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, f"{symbol}.csv")

daily_data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
hourly_data = yf.download(symbol, start=start_date, end=end_date, interval="1h")

def identify_resistance(data, window=20):
    data['Resistance'] = data['High'].rolling(window=window).max()
    return data
    
daily_data = identify_resistance(daily_data, window)

def detect_breakouts(hourly_data, resistance_level):
    breakouts = hourly_data[hourly_data['Close'] > resistance_level]
    return breakouts

most_recent_resistance = daily_data['Resistance'].iloc[-1]

hourly_breakouts = detect_breakouts(hourly_data, most_recent_resistance)

def place_orders_and_backtest(breakouts, hourly_data):
    results = []
    for _, breakout in breakouts.iterrows():
        entry_time = breakout.name
        entry_price = breakout['Close']
        
        subsequent_candles = hourly_data.loc[hourly_data.index > entry_time]
        if not subsequent_candles.empty:
            subsequent_candle = subsequent_candles.iloc[0]
            exit_price = subsequent_candle['Close']
            profit = exit_price - entry_price
            
            result = {
                'entry_time': entry_time,
                'entry_price': entry_price,
                'exit_time': subsequent_candle.name,
                'exit_price': exit_price,
                'profit': profit
            }
            results.append(result)

    return results

backtest_results = place_orders_and_backtest(hourly_breakouts, hourly_data)

results_df = pd.DataFrame(backtest_results)

if not results_df.empty:
    total_profit = results_df['profit'].sum()
    initial_investment = len(results_df) * results_df['entry_price'].mean()  # Average entry price for initial investment
    overall_profit_margin = (total_profit / initial_investment) * 100 if initial_investment > 0 else 0
else:
    total_profit = 0
    overall_profit_margin = 0

results_df.to_csv(output_file, index=False)

print(f"\nResults exported to {output_file}.")
print(f"Overall Profit Margin: {overall_profit_margin:.2f}%")


