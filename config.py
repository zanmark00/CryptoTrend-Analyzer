import os

# Determine the project's base directory (config.py is in the root folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
VISUALIZATION_DIR = os.path.join(DATA_DIR, "visualizations")
COMBINED_DATA_DIR = os.path.join(DATA_DIR, "combined")
PREPROCESSED_PATH = os.path.join(DATA_DIR, "preprocessed")

# Automatically create directories if they don't exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, VISUALIZATION_DIR, COMBINED_DATA_DIR, PREPROCESSED_PATH]:
    os.makedirs(dir_path, exist_ok=True)

# API Credentials and Endpoints

# Reddit API credentials
REDDIT_API_CREDENTIALS = {
    "client_id": "your_reddit_client_id",         # Replace with your Reddit client ID
    "client_secret": "your_reddit_client_secret",   # Replace with your Reddit client secret
    "user_agent": "CryptoTrendAnalyzer/0.1 by your_username"  # Replace 'your_username' as appropriate
}

# NewsAPI key
NEWSAPI_KEY = "your_newsapi_key"  # Replace with your NewsAPI key

# API Endpoints
API_ENDPOINTS = {
    "coingecko": "https://api.coingecko.com/api/v3/coins/markets",
    "binance": "https://api.binance.com/api/v3/ticker/price",
    "fear_greed": "https://api.alternative.me/fng/"
}

# MongoDB Configuration (if applicable)
MONGO_CONFIG = {
    "uri": "your_mongodb_uri",                # e.g., "mongodb://localhost:27017/"
    "db_name": "your_database_name",          # Replace with your MongoDB database name
    "collection_name": "your_collection_name" # Replace with your MongoDB collection name
}