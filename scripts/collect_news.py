import os
import requests
import pandas as pd
from config import NEWSAPI_KEY, RAW_DATA_DIR

# Define keywords to search for (adjust as needed)
KEYWORDS = ["bitcoin", "crypto", "ethereum"]

def fetch_crypto_news(keyword="crypto"):
    """
    Fetch crypto-related news articles using NewsAPI and save as a CSV.
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
        df = pd.DataFrame(articles)
        output_path = os.path.join(RAW_DATA_DIR, "news_articles.csv")
        df.to_csv(output_path, index=False)
        print(f"News articles ({keyword}) saved to: {output_path}")
    except Exception as e:
        print(f"Error fetching news articles for '{keyword}': {e}")

if __name__ == "__main__":
    for kw in KEYWORDS:
        fetch_crypto_news(kw)