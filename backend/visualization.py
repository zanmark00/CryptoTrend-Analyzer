import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the config module
try:
    import config
except ImportError as e:
    print("Error importing config module. Ensure that config.py is in the correct directory.")
    raise e

def load_csv_safe(file_path):
    """Safely load a CSV file."""
    print(f"Loading file: {file_path}")  # Debugging statement
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    else:
        print(f"File not found: {file_path}")
        return None

def plot_coingecko(ax):
    """Plot Top 10 Cryptos by 24h % Change from CoinGecko data."""
    coingecko_file = os.path.join(config.RAW_DATA_DIR, "coingecko_prices.csv")
    df = load_csv_safe(coingecko_file)
    if df is not None and not df.empty:
        df = df.dropna(subset=["price_change_percentage_24h"])
        top10 = df.sort_values(by="price_change_percentage_24h", ascending=False).head(10)
        sns.barplot(data=top10, x="name", y="price_change_percentage_24h", palette="coolwarm", ax=ax, hue="name")
        ax.set_title("Top 10 Cryptos by 24h % Change (CoinGecko)")
        ax.set_xlabel("Crypto Name")
        ax.set_ylabel("24h % Change")
        ax.tick_params(axis='x', rotation=45)
    else:
        ax.text(0.5, 0.5, "No CoinGecko data available", horizontalalignment='center', verticalalignment='center')

def plot_fear_greed(ax):
    """Plot the Fear & Greed Index."""
    fear_greed_file = os.path.join(config.RAW_DATA_DIR, "fear_greed_index.csv")
    df = load_csv_safe(fear_greed_file)
    if df is not None and not df.empty:
        value = df.iloc[0]["value"]
        classification = df.iloc[0]["value_classification"]
        ax.barh([0], [value], color="skyblue")
        ax.set_xlim(0, 100)
        ax.set_yticks([])
        ax.set_title("Fear & Greed Index")
        ax.set_xlabel(f"Index Value: {value} ({classification})")
        ax.text(value/2, 0, f"{value} - {classification}", va='center', ha='center', fontsize=12, color='black')
    else:
        ax.text(0.5, 0.5, "No Fear & Greed data available", horizontalalignment='center', verticalalignment='center')

def plot_reddit_keywords(ax):
    """Plot Top 10 Reddit Keywords."""
    reddit_file = os.path.join(config.RAW_DATA_DIR, "reddit_posts.csv")
    df = load_csv_safe(reddit_file)
    if df is not None and not df.empty:
        keyword_freq = df["keyword"].value_counts().reset_index()
        keyword_freq.columns = ["keyword", "count"]
        top_keywords = keyword_freq.head(10)
        sns.barplot(data=top_keywords, x="keyword", y="count", palette="magma", ax=ax, hue="keyword")
        ax.set_title("Top 10 Reddit Keywords")
        ax.set_xlabel("Keyword")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis='x', rotation=45)
    else:
        ax.text(0.5, 0.5, "No Reddit data available", horizontalalignment='center', verticalalignment='center')

def main():
    """Main function to create the plots."""
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    plot_coingecko(axs[0])
    plot_fear_greed(axs[1])
    plot_reddit_keywords(axs[2])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()