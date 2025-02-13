import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import config

def load_csv_safe(file_path, parse_dates=None):
    """Safely load a CSV file, optionally parsing specified columns as dates."""
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path, parse_dates=parse_dates)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    else:
        print(f"File not found: {file_path}")
        return None

def plot_coingecko(ax):
    """Panel 1: Plot Top 10 Cryptos by 24h % Change from CoinGecko data."""
    coingecko_file = os.path.join(config.RAW_DATA_DIR, "coingecko_prices.csv")
    df = load_csv_safe(coingecko_file)
    if df is not None and not df.empty:
        df = df.dropna(subset=["price_change_percentage_24h"])
        top10 = df.sort_values(by="price_change_percentage_24h", ascending=False).head(10)
        sns.barplot(data=top10, x="name", y="price_change_percentage_24h", palette="coolwarm", ax=ax)
        ax.set_title("Top 10 Cryptos by 24h % Change (CoinGecko)")
        ax.set_xlabel("Crypto Name")
        ax.set_ylabel("24h % Change")
        ax.tick_params(axis='x', rotation=45)
    else:
        ax.text(0.5, 0.5, "No CoinGecko data available",
                horizontalalignment='center', verticalalignment='center')

def plot_fear_greed(ax):
    """Panel 2: Plot the Fear & Greed Index."""
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
        ax.text(0.5, 0.5, "No Fear & Greed data available",
                horizontalalignment='center', verticalalignment='center')

def plot_reddit_keywords(ax):
    """Panel 3: Plot Top 10 Reddit Keywords."""
    reddit_file = os.path.join(config.RAW_DATA_DIR, "reddit_posts.csv")
    df = load_csv_safe(reddit_file)
    if df is not None and not df.empty:
        keyword_freq = df["keyword"].value_counts().reset_index()
        keyword_freq.columns = ["keyword", "count"]
        top_keywords = keyword_freq.head(10)
        sns.barplot(data=top_keywords, x="keyword", y="count", palette="magma", ax=ax)
        ax.set_title("Top 10 Reddit Keywords")
        ax.set_xlabel("Keyword")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis='x', rotation=45)
    else:
        ax.text(0.5, 0.5, "No Reddit data available",
                horizontalalignment='center', verticalalignment='center')

def plot_yahoo_prices(ax):
    """Panel 4: Plot Yahoo Crypto Closing Prices Trend."""
    yahoo_file = os.path.join(config.RAW_DATA_DIR, "yahoo_crypto.csv")
    df = load_csv_safe(yahoo_file, parse_dates=["Date"])
    if df is not None and not df.empty:
        df = df.sort_values(by="Date")
        ax.plot(df["Date"], df["Close"], marker='o', linestyle='-', color="green")
        ax.set_title("Yahoo Crypto Closing Prices")
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price")
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    else:
        ax.text(0.5, 0.5, "No Yahoo Finance data available",
                horizontalalignment='center', verticalalignment='center')

def plot_news_volume(ax):
    """Panel 5: Plot News Articles Volume Over Time."""
    news_file = os.path.join(config.RAW_DATA_DIR, "news_articles.csv")
    df = load_csv_safe(news_file, parse_dates=["publishedAt"])
    if df is not None and not df.empty:
        df["date"] = pd.to_datetime(df["publishedAt"]).dt.date
        news_volume = df.groupby("date").size().reset_index(name="count")
        news_volume = news_volume.sort_values(by="date")
        ax.plot(news_volume["date"], news_volume["count"], marker='o', linestyle='-', color="purple")
        ax.set_title("News Articles Volume Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Article Count")
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    else:
        ax.text(0.5, 0.5, "No news articles data available",
                horizontalalignment='center', verticalalignment='center')

def plot_binance_snapshot(ax):
    """Panel 6: Plot Binance Prices Snapshot (Top 10)."""
    binance_file = os.path.join(config.RAW_DATA_DIR, "binance_prices.csv")
    df = load_csv_safe(binance_file)
    if df is not None and not df.empty:
        top_binance = df.sort_values(by="price", ascending=False).head(10)
        sns.barplot(data=top_binance, x="symbol", y="price", palette="Blues_d", ax=ax)
        ax.set_title("Binance Prices Snapshot (Top 10)")
        ax.set_xlabel("Symbol")
        ax.set_ylabel("Price")
        ax.tick_params(axis='x', rotation=45)
    else:
        ax.text(0.5, 0.5, "No Binance data available",
                horizontalalignment='center', verticalalignment='center')

def visualize_comprehensive_trends():
    """Creates a 2x3 grid with various panels covering multiple data trends."""
    sns.set_theme(style="whitegrid")
    
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 12))
    
    # Panel 1: CoinGecko Top 10 24h % Change
    plot_coingecko(axes[0, 0])
    # Panel 2: Fear & Greed Index
    plot_fear_greed(axes[0, 1])
    # Panel 3: Top 10 Reddit Keywords
    plot_reddit_keywords(axes[0, 2])
    # Panel 4: Yahoo Crypto Closing Prices Trend
    plot_yahoo_prices(axes[1, 0])
    # Panel 5: News Articles Volume Over Time
    plot_news_volume(axes[1, 1])
    # Panel 6: Binance Prices Snapshot (Top 10)
    plot_binance_snapshot(axes[1, 2])
    
    plt.tight_layout()
    os.makedirs(config.VISUALIZATION_DIR, exist_ok=True)
    output_file = os.path.join(config.VISUALIZATION_DIR, "comprehensive_trends.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Comprehensive trends visualization saved to {output_file}")

def main():
    print("Starting comprehensive visualization of trends...")
    visualize_comprehensive_trends()
    print("Visualization complete.")

if __name__ == "__main__":
    main()