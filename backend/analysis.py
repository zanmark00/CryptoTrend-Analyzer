import sys
import os
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RAW_DATA_DIR, VISUALIZATION_DIR  # Ensure these paths are correctly defined in config.py

def normalize(series):
    """
    Apply min–max normalization on a pandas Series.
    If the min and max are equal, return the original series.
    """
    if series.max() - series.min() == 0:
        return series
    return (series - series.min()) / (series.max() - series.min())

def get_trending_coins():
    """
    Loads CoinGecko data and Reddit posts data to compute a composite score for each coin.
    The composite score is defined as the sum of the normalized 24h price change percentage
    and normalized Reddit post count.
    
    Returns the top 5 coins ranked by composite score.
    """
    # Load CoinGecko market data
    coingecko_path = os.path.join(RAW_DATA_DIR, "coingecko_prices.csv")
    try:
        df_geo = pd.read_csv(coingecko_path)
    except Exception as e:
        print(f"Error loading {coingecko_path}: {e}")
        return None

    # Drop rows missing a valid 24h price change and keep only coins with positive changes
    df_geo = df_geo.dropna(subset=["price_change_percentage_24h"])
    df_geo = df_geo[df_geo["price_change_percentage_24h"] > 0].copy()
    # Normalize coin names: lower-case and remove extraneous whitespace
    df_geo["name_lower"] = df_geo["name"].str.lower().str.strip()

    # Load Reddit posts data
    reddit_path = os.path.join(RAW_DATA_DIR, "reddit_posts.csv")
    try:
        df_reddit = pd.read_csv(reddit_path)
    except Exception as e:
        print(f"Error loading {reddit_path}: {e}")
        return None

    df_reddit["keyword_lower"] = df_reddit["keyword"].str.lower().str.strip()
    # Count Reddit posts per keyword
    reddit_counts = df_reddit.groupby("keyword_lower").size().reset_index(name="reddit_count")

    # Merge market data with Reddit counts on the normalized coin name / keyword
    df_merged = pd.merge(df_geo, reddit_counts, how="left", left_on="name_lower", right_on="keyword_lower")
    # Convert reddit_count to numeric and fill missing counts with 0
    df_merged["reddit_count"] = pd.to_numeric(df_merged["reddit_count"], errors="coerce").fillna(0)

    # Normalize the key metrics
    df_merged["norm_price_change"] = normalize(df_merged["price_change_percentage_24h"])
    df_merged["norm_reddit_count"] = normalize(df_merged["reddit_count"])

    # Calculate the composite score as the sum of the normalized price change and Reddit count
    df_merged["composite_score"] = df_merged["norm_price_change"] + df_merged["norm_reddit_count"]

    # Sort by composite score (highest first) and take the top 5 coins
    df_sorted = df_merged.sort_values("composite_score", ascending=False)
    trending_coins = df_sorted.head(5)

    return trending_coins

def create_trending_visualizations(trending_coins):
    """
    Creates two visualizations and saves them to VISUALIZATION_DIR:
      1. A bar plot of the composite scores for the trending coins.
      2. A pie chart for the Reddit post distribution among the trending coins.
    """
    # Ensure that the visualizations folder exists
    if not os.path.exists(VISUALIZATION_DIR):
        os.makedirs(VISUALIZATION_DIR)

    # Visualization 1: Bar plot for composite scores
    try:
        plt.figure(figsize=(10, 6))
        # Sort so that the coin with the lowest composite score appears at the bottom
        trending_sorted = trending_coins.sort_values("composite_score", ascending=True)
        # Use the "name" column as both y and hue (required by Seaborn) and then remove the legend.
        ax = sns.barplot(x="composite_score", y="name", data=trending_sorted,
                         hue="name", palette="viridis", dodge=False)
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
        plt.xlabel("Composite Score")
        plt.ylabel("Coin")
        plt.title("Trending Coins by Composite Score")
        plt.tight_layout()
        bar_plot_path = os.path.join(VISUALIZATION_DIR, "trending_coins_bar.png")
        plt.savefig(bar_plot_path)
        plt.close()
        print(f"Trending coins bar plot saved to: {bar_plot_path}")
    except Exception as e:
        print("Error creating bar plot visualization:")
        print(traceback.format_exc())

    # Visualization 2: Pie chart for Reddit post distribution
    try:
        # Ensure no NaN values remain
        trending_coins["reddit_count"] = pd.to_numeric(trending_coins["reddit_count"], errors="coerce").fillna(0)
        total_reddit = trending_coins["reddit_count"].sum()
        if total_reddit <= 0:
            print("Warning: Sum of reddit_count values is zero. Skipping pie chart visualization.")
        else:
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
    except Exception as e:
        print("Error creating pie chart visualization:")
        print(traceback.format_exc())

if __name__ == "__main__":
    trending_coins = get_trending_coins()
    if trending_coins is not None and not trending_coins.empty:
        print("Trending coins data collected:")
        print(trending_coins[['name', 'price_change_percentage_24h', 'reddit_count', 'composite_score']])
        create_trending_visualizations(trending_coins)
    else:
        print("No trending coins data available.")