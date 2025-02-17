import sys
import os
# Add the project root (parent directory) to sys.path so that config.py can be imported.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import praw
from config import RAW_DATA_DIR, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

def fetch_reddit_posts(subreddit="cryptocurrency", limit=1000, queries=None):
    """
    Fetch Reddit posts based on a list of search queries and save them as a CSV file.
    Each query will be used to search the specified subreddit, and the posts returned will have
    the 'keyword' field set to the query that fetched them.
    
    Parameters:
        subreddit (str): The subreddit to search in.
        limit (int): The maximum number of posts to fetch per query.
        queries (list): A list of keywords to search for. Defaults to a predefined list if None.
    """
    if queries is None:
        # Default list of keywords; feel free to modify this list.
        queries = ["bitcoin", "ethereum", "ripple", "litecoin", "cardano"]

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        records = []
        for query in queries:
            print(f"Fetching posts for keyword: {query}")
            posts = reddit.subreddit(subreddit).search(query, limit=limit)
            for post in posts:
                records.append({
                    "keyword": query,
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "num_comments": post.num_comments,
                    "created": post.created_utc,
                    "author": str(post.author) if post.author else None,
                    "subreddit": str(post.subreddit)
                })
        df = pd.DataFrame(records)
        output_path = os.path.join(RAW_DATA_DIR, "reddit_posts.csv")
        df.to_csv(output_path, index=False)
        print(f"Reddit posts saved to: {output_path}")
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")

if __name__ == "__main__":
    fetch_reddit_posts()