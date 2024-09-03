import pandas as pd
import os

def main():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop, "data.csv")
    
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        print("Existing data.csv file loaded successfully.")
    else:
        print("data.csv file does not exist. Creating a new file.")
        df = pd.DataFrame(columns=['stock_ticker', 'RSI', 'CIV', 'SMA', 'ATR', 'is_breakout'])

    new_rows = [] 

    while True:
        stock_ticker = input("Enter stock ticker (or type 'done' to finish): ").strip()
        if stock_ticker.lower() == 'done':
            break
        
        try:
            rsi = float(input("Enter RSI value: ").strip())
            civ = float(input("Enter CIV value: ").strip())
            sma = float(input("Enter SMA value: ").strip())
            atr = float(input("Enter ATR value: ").strip())
            is_breakout = int(input("Enter is_breakout value (0 or 1): ").strip())
            if is_breakout not in [0, 1]:
                raise ValueError("is_breakout must be 0 or 1.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
            continue

        new_rows.append({
            'stock_ticker': stock_ticker,
            'RSI': rsi,
            'CIV': civ,
            'SMA': sma,
            'ATR': atr,
            'is_breakout': is_breakout
        })

    new_df = pd.DataFrame(new_rows)

    df = pd.concat([df, new_df], ignore_index=True)

    df.to_csv(file_path, index=False)
    print(f"Data has been saved to 'data.csv' on your desktop.")

if __name__ == "__main__":
    main()
