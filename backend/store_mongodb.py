import os
import pandas as pd
from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME, PROCESSED_DATA_DIR

def store_data_to_mongo():
    """
    Load processed data (for example, the merged Yahoo and Fear & Greed dataset)
    into a MongoDB collection.
    """
    combined_file = os.path.join(PROCESSED_DATA_DIR, "yahoo_fgi_merged.csv")
    try:
        df = pd.read_csv(combined_file)
    except Exception as e:
        print(f"Error reading {combined_file}: {e}")
        return

    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]
        records = df.to_dict(orient='records')
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} documents into MongoDB collection '{MONGO_COLLECTION_NAME}'.")
    except Exception as e:
        print(f"Error storing data to MongoDB: {e}")

if __name__ == "__main__":
    store_data_to_mongo()