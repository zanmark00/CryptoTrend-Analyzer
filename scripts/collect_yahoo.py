import os
import pandas as pd
import yfinance as yf
from config import RAW_DATA_DIR

def fetch_yahoo_data(ticker="BTC-USD", period="max"):
    """
    Fetch Yahoo Finance data for a given ticker and save it as a CSV file.
    """
    try:
        df = yf.download(ticker, period=period)
        df.reset_index(inplace=True)
        output_path = os.path.join(RAW_DATA_DIR, "yahoo_crypto.csv")
        df.to_csv(output_path, index=False)
        print(f"Yahoo Finance data for {ticker} saved to: {output_path}")
    except Exception as e:
        print(f"Error fetching Yahoo Finance data: {e}")

if __name__ == "__main__":
    fetch_yahoo_data()