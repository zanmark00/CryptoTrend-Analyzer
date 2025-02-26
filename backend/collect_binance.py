import sys
import os
import requests
import pandas as pd

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import BINANCE_API_URL, RAW_DATA_DIR

# Rest of your code here...
print("BINANCE_API_URL:", BINANCE_API_URL)
print("RAW_DATA_DIR:", RAW_DATA_DIR)
# ... (continue with data collection logic)

def fetch_binance_prices():
    """
    Fetch Binance price data from the API and save it as a CSV file.
    """
    try:
        response = requests.get(BINANCE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        
        output_path = os.path.join(RAW_DATA_DIR, "binance_prices.csv")
        df.to_csv(output_path, index=False)
        print(f"Binance prices saved to: {output_path}")
    except Exception as e:
        print(f"Error fetching Binance prices: {e}")

if __name__ == "__main__":
    fetch_binance_prices()