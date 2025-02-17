import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import pandas as pd
from config import FEAR_GREED_API_URL, RAW_DATA_DIR

def fetch_fear_greed_index():
    """
    Fetch the Fear & Greed Index data and save it as a CSV file in the raw data directory.
    """
    try:
        response = requests.get(FEAR_GREED_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        # If the API returns data nested under a "data" key, extract it; otherwise use the full JSON.
        index_data = data.get("data", data)
        df = pd.DataFrame(index_data)
        output_path = os.path.join(RAW_DATA_DIR, "fear_greed_index.csv")
        df.to_csv(output_path, index=False)
        print(f"Fear & Greed Index data saved to: {output_path}")
    except Exception as e:
        print(f"Error fetching Fear & Greed data: {e}")

if __name__ == "__main__":
    fetch_fear_greed_index()