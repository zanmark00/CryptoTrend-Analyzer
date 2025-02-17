import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import COMBINED_DATA_DIR, PROCESSED_DATA_DIR

def eda_summary():
    """
    Perform exploratory data analysis (EDA) on the combined dataset if available;
    otherwise, analyze the Yahoo Finance data.
    """
    combined_file = os.path.join(COMBINED_DATA_DIR, "crypto_combined.csv")
    if os.path.exists(combined_file):
        df = pd.read_csv(combined_file)
        print("Combined Dataset Summary:")
    else:
        yahoo_file = os.path.join(PROCESSED_DATA_DIR, "yahoo_crypto_cleaned.csv")
        try:
            df = pd.read_csv(yahoo_file)
        except Exception as e:
            print(f"Error reading {yahoo_file}: {e}")
            return
        print("Yahoo Crypto Data Summary:")

    print(df.info())
    print(df.describe())
    
    # Plot a correlation heatmap for numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if not numeric_cols.empty:
        corr = df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.show()
    else:
        print("No numeric columns found for correlation heatmap.")

if __name__ == "__main__":
    eda_summary()