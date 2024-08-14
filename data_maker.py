import pandas as pd
import os

def main():
    # Path to the data.csv file on the desktop
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop, "data.csv")

    # Load the existing CSV file into a DataFrame
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        print("Existing data.csv file loaded successfully.")
    else:
        print("data.csv file does not exist. Creating a new file.")
        # Create an empty DataFrame with the expected columns
        df = pd.DataFrame(columns=['stock_ticker', 'RSI', 'CIV', 'SMA', 'ATR', 'is_breakout'])

    new_rows = []  # List to collect new rows

    while True:
        # Prompt user for input for each column
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

        # Collect the input values as a dictionary
        new_rows.append({
            'stock_ticker': stock_ticker,
            'RSI': rsi,
            'CIV': civ,
            'SMA': sma,
            'ATR': atr,
            'is_breakout': is_breakout
        })

    # Convert the list of new rows to a DataFrame
    new_df = pd.DataFrame(new_rows)

    # Append the new DataFrame to the existing one
    df = pd.concat([df, new_df], ignore_index=True)

    # Save the updated DataFrame back to data.csv
    df.to_csv(file_path, index=False)
    print(f"Data has been saved to 'data.csv' on your desktop.")

if __name__ == "__main__":
    main()
