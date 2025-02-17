import sys
import os
# Add the project root (parent directory) to sys.path so that config.py can be found.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import pandas as pd
from config import COINGECKO_API_URL, RAW_DATA_DIR

def fetch_coingecko_data():
    """
    Fetch CoinGecko data and save it as a CSV file in the raw data directory.
    """
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "sparkline": "false",
    }
    all_data = []
    try:
        # Paginate to get ~750 entries (adjust as needed)
        for page in range(1, 4):
            params["page"] = page
            response = requests.get(COINGECKO_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data)
        
        if not all_data:
            print("No data fetched from the CoinGecko API.")
            return
        
        df = pd.DataFrame(all_data)
        output_path = os.path.join(RAW_DATA_DIR, "coingecko_prices.csv")
        df.to_csv(output_path, index=False)
        print(f"CoinGecko data saved to: {output_path}")
    except Exception as e:
        print(f"Error fetching CoinGecko data: {e}")

if __name__ == "__main__":
    fetch_coingecko_data()