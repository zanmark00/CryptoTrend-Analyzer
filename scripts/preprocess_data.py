import os
import pandas as pd
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR

# Ensure the processed data directory exists
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def preprocess_yahoo():
    """
    Preprocess the Yahoo Finance crypto data:
    - Convert 'Date' to datetime.
    - Create 'Date_only' for merging.
    - Drop invalid rows.
    - Save cleaned data.
    """
    yahoo_file = os.path.join(RAW_DATA_DIR, "yahoo_crypto.csv")
    try:
        yahoo_df = pd.read_csv(yahoo_file)
    except Exception as e:
        print(f"Failed to read {yahoo_file}: {e}")
        return
    yahoo_df['Date'] = pd.to_datetime(yahoo_df['Date'], utc=True, errors='coerce')
    yahoo_df['Date_only'] = yahoo_df['Date'].dt.date
    yahoo_df = yahoo_df.dropna(subset=['Date'])
    output_file = os.path.join(PROCESSED_DATA_DIR, "yahoo_crypto_cleaned.csv")
    yahoo_df.to_csv(output_file, index=False)
    print(f"Cleaned Yahoo Finance data saved to {output_file}")

def preprocess_fear_greed():
    """
    Preprocess the Fear & Greed Index data:
    - Convert timestamp using unit 's'.
    - Create a date column.
    - Save cleaned data.
    """
    fgi_file = os.path.join(RAW_DATA_DIR, "fear_greed_index.csv")
    try:
        fgi_df = pd.read_csv(fgi_file)
    except Exception as e:
        print(f"Failed to read {fgi_file}: {e}")
        return
    fgi_df['datetime'] = pd.to_datetime(fgi_df['timestamp'], unit='s', errors='coerce')
    fgi_df['Date'] = fgi_df['datetime'].dt.date
    output_file = os.path.join(PROCESSED_DATA_DIR, "fear_greed_index_cleaned.csv")
    fgi_df.to_csv(output_file, index=False)
    print(f"Cleaned Fear & Greed data saved to {output_file}")

def merge_yahoo_fgi():
    """
    Merge cleaned Yahoo Finance and Fear & Greed data on the date column.
    """
    yahoo_file = os.path.join(PROCESSED_DATA_DIR, "yahoo_crypto_cleaned.csv")
    fgi_file = os.path.join(PROCESSED_DATA_DIR, "fear_greed_index_cleaned.csv")
    try:
        yahoo_df = pd.read_csv(yahoo_file)
        fgi_df = pd.read_csv(fgi_file)
    except Exception as e:
        print(f"Error reading cleaned files: {e}")
        return
    merged_df = pd.merge(yahoo_df, fgi_df, left_on='Date_only', right_on='Date', how='left')
    output_file = os.path.join(PROCESSED_DATA_DIR, "yahoo_fgi_merged.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"Merged data saved to {output_file}")

def preprocess_binance():
    """
    Read Binance prices CSV and save a cleaned copy.
    """
    binance_file = os.path.join(RAW_DATA_DIR, "binance_prices.csv")
    try:
        binance_df = pd.read_csv(binance_file)
    except Exception as e:
        print(f"Failed to read {binance_file}: {e}")
        return
    output_file = os.path.join(PROCESSED_DATA_DIR, "binance_prices_cleaned.csv")
    binance_df.to_csv(output_file, index=False)
    print(f"Cleaned Binance data saved to {output_file}")

def preprocess_coingecko():
    """
    Read CoinGecko prices CSV and save a cleaned copy.
    """
    coingecko_file = os.path.join(RAW_DATA_DIR, "coingecko_prices.csv")
    try:
        cg_df = pd.read_csv(coingecko_file)
    except Exception as e:
        print(f"Failed to read {coingecko_file}: {e}")
        return
    output_file = os.path.join(PROCESSED_DATA_DIR, "coingecko_prices_cleaned.csv")
    cg_df.to_csv(output_file, index=False)
    print(f"Cleaned CoinGecko data saved to {output_file}")

def preprocess_news():
    """
    Preprocess news articles data:
    - Convert 'publishedAt' to datetime.
    - Save cleaned data.
    """
    news_file = os.path.join(RAW_DATA_DIR, "news_articles.csv")
    try:
        news_df = pd.read_csv(news_file)
    except Exception as e:
        print(f"Failed to read {news_file}: {e}")
        return
    news_df['publishedAt'] = pd.to_datetime(news_df['publishedAt'], errors='coerce')
    output_file = os.path.join(PROCESSED_DATA_DIR, "news_articles_cleaned.csv")
    news_df.to_csv(output_file, index=False)
    print(f"Cleaned news data saved to {output_file}")

def preprocess_reddit():
    """
    Preprocess Reddit posts data:
    - Convert 'created' to datetime.
    - Save cleaned data.
    """
    reddit_file = os.path.join(RAW_DATA_DIR, "reddit_posts.csv")
    try:
        reddit_df = pd.read_csv(reddit_file)
    except Exception as e:
        print(f"Failed to read {reddit_file}: {e}")
        return
    reddit_df['created'] = pd.to_datetime(reddit_df['created'], errors='coerce')
    output_file = os.path.join(PROCESSED_DATA_DIR, "reddit_posts_cleaned.csv")
    reddit_df.to_csv(output_file, index=False)
    print(f"Cleaned Reddit posts data saved to {output_file}")

if __name__ == "__main__":
    preprocess_yahoo()
    preprocess_fear_greed()
    merge_yahoo_fgi()
    preprocess_binance()
    preprocess_coingecko()
    preprocess_news()
    preprocess_reddit()
    print("All preprocessing complete.")