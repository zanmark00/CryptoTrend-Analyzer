import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import RAW_DATA_DIR, VISUALIZATION_DIR  # Import paths from config.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def normalize(series):
    """
    Apply min–max normalization on a pandas Series.
    If min and max are equal, returns the original series.
    """
    if series.max() - series.min() == 0:
        return series
    return (series - series.min()) / (series.max() - series.min())

def get_trending_coins():
    """
    Loads CoinGecko data and Reddit posts data to compute a composite score
    for each coin. The composite score is calculated as the sum of the normalized
    24h price change percentage and normalized Reddit post count.
    
    Returns a DataFrame of the top 5 coins by composite score (trending coins).
    """
    # Load CoinGecko market data
    coingecko_path = os.path.join(RAW_DATA_DIR, "coingecko_prices.csv")
    try:
        df_geo = pd.read_csv(coingecko_path)
    except Exception as e:
        print(f"Error loading {coingecko_path}: {e}")
        return None

    # Drop rows without a valid 24h price change and keep positive changes only
    df_geo = df_geo.dropna(subset=["price_change_percentage_24h"])
    df_geo = df_geo[df_geo["price_change_percentage_24h"] > 0].copy()
    df_geo["name_lower"] = df_geo["name"].str.lower()

    # Load Reddit posts data (sentiment indicator)
    reddit_path = os.path.join(RAW_DATA_DIR, "reddit_posts.csv")
    try:
        df_reddit = pd.read_csv(reddit_path)
    except Exception as e:
        print(f"Error loading {reddit_path}: {e}")
        return None

    df_reddit["keyword_lower"] = df_reddit["keyword"].str.lower()
    # Count Reddit posts per keyword
    reddit_counts = df_reddit.groupby("keyword_lower").size().reset_index(name="reddit_count")

    # Merge market data with Reddit counts
    df_merged = pd.merge(df_geo, reddit_counts, how="left", left_on="name_lower", right_on="keyword_lower")
    df_merged["reddit_count"] = df_merged["reddit_count"].fillna(0)

    # Normalize the key metrics
    df_merged["norm_price_change"] = normalize(df_merged["price_change_percentage_24h"])
    df_merged["norm_reddit_count"] = normalize(df_merged["reddit_count"])

    # Compute the composite score (equal weights)
    df_merged["composite_score"] = df_merged["norm_price_change"] + df_merged["norm_reddit_count"]

    # Sort by composite score in descending order and extract the top 5 as trending coins
    df_sorted = df_merged.sort_values("composite_score", ascending=False)
    trending_coins = df_sorted.head(5)

    return trending_coins

def create_trending_visualizations(trending_coins):
    """
    Creates visualizations for trending coins and saves the plots in the visualizations folder.
    
    Visualizations:
      1. Bar plot of the composite scores for the trending coins.
      2. Pie chart showing the distribution of Reddit post counts among the trending coins.
    """
    # Ensure the visualizations folder exists
    if not os.path.exists(VISUALIZATION_DIR):
        os.makedirs(VISUALIZATION_DIR)

    # Visualization 1: Bar plot for trending coins (Composite Score)
    plt.figure(figsize=(10, 6))
    # Sort trending coins so the lowest score is at the bottom
    trending_sorted = trending_coins.sort_values("composite_score", ascending=True)
    sns.barplot(x="composite_score", y="name", data=trending_sorted, palette="viridis")
    plt.xlabel("Composite Score")
    plt.ylabel("Coin")
    plt.title("Trending Coins by Composite Score")
    plt.tight_layout()
    bar_plot_path = os.path.join(VISUALIZATION_DIR, "trending_coins_bar.png")
    plt.savefig(bar_plot_path)
    plt.close()
    print(f"Trending coins bar plot saved to: {bar_plot_path}")

    # Visualization 2: Pie chart for Reddit post distribution among trending coins
    plt.figure(figsize=(8, 8))
    plt.pie(trending_coins["reddit_count"],
            labels=trending_coins["name"],
            autopct="%1.1f%%",
            startangle=140)
    plt.title("Reddit Post Distribution among Trending Coins")
    plt.tight_layout()
    pie_chart_path = os.path.join(VISUALIZATION_DIR, "trending_coins_reddit_pie.png")
    plt.savefig(pie_chart_path)
    plt.close()
    print(f"Trending coins Reddit distribution pie chart saved to: {pie_chart_path}")

if __name__ == "__main__":
    trending_coins = get_trending_coins()
    if trending_coins is not None and not trending_coins.empty:
        create_trending_visualizations(trending_coins)
    else:
        print("No trending coins data available.")