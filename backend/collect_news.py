import sys
import os
# Add the project root (parent directory) to sys.path so that config.py can be found.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import pandas as pd
from config import NEWSAPI_KEY, RAW_DATA_DIR

# Define keywords to search for (adjust as needed)
KEYWORDS = ["bitcoin", "crypto", "ethereum"]

def fetch_crypto_news(keyword="crypto"):
    """
    Fetch crypto-related news articles using NewsAPI for the given keyword
    and save them as a CSV file.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "apiKey": NEWSAPI_KEY,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 100
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            print(f"No articles found for keyword '{keyword}'.")
            return None

        df = pd.DataFrame(articles)
        # Save each keyword's news to a separate file to prevent overwriting.
        output_path = os.path.join(RAW_DATA_DIR, f"news_articles_{keyword}.csv")
        df.to_csv(output_path, index=False)
        print(f"News articles for '{keyword}' saved to: {output_path}")
        return df

    except Exception as e:
        print(f"Error fetching news articles for '{keyword}': {e}")
        return None

if __name__ == "__main__":
    # Fetch news articles for each keyword and combine the results
    combined_dfs = []
    for kw in KEYWORDS:
        df = fetch_crypto_news(kw)
        if df is not None:
            combined_dfs.append(df)

    if combined_dfs:
        combined_df = pd.concat(combined_dfs, ignore_index=True)
        combined_output_path = os.path.join(RAW_DATA_DIR, "news_articles_combined.csv")
        combined_df.to_csv(combined_output_path, index=False)
        print(f"Combined news articles saved to: {combined_output_path}")