import os
import sys
import subprocess
import logging
import base64
from flask import Flask, render_template_string
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO

# Set up logging.
logging.basicConfig(level=logging.DEBUG)

# Determine the project root and update sys.path.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Import config (ensure config.py defines RAW_DATA_DIR and VISUALIZATION_DIR)
import config

app = Flask(__name__)

def embed_image(image_path):
    """
    Reads an image file and returns a base64-encoded data URI.
    If the image does not exist, returns None.
    """
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return None

# A common base HTML template with header, navigation, and footer.
base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <style>
    /* Reset and global styles */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
      color: #333;
    }
    header {
      background: #4A90E2;
      padding: 20px;
      text-align: center;
      color: white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    nav {
      background: #fff;
      padding: 10px;
      text-align: center;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    nav a {
      text-decoration: none;
      margin: 0 15px;
      font-size: 16px;
      color: #4A90E2;
      padding: 8px 16px;
      border-radius: 5px;
      transition: background 0.3s, color 0.3s;
    }
    nav a:hover {
      background: #4A90E2;
      color: #fff;
    }
    .container {
      max-width: 1100px;
      margin: 40px auto;
      padding: 20px;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
      margin-bottom: 20px;
      color: #333;
    }
    p {
      margin-bottom: 15px;
      line-height: 1.6;
    }
    ul {
      margin-left: 20px;
      margin-bottom: 15px;
    }
    li {
      margin-bottom: 8px;
    }
    .flex-container {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-around;
      gap: 20px;
    }
    .flex-item {
      flex: 1 1 300px;
      text-align: center;
      background: #f8f9fa;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    footer {
      text-align: center;
      padding: 20px;
      background: #f0f0f0;
      font-size: 14px;
      color: #777;
    }
    img {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <header>
    <h1>CryptoTrend Analyzer</h1>
  </header>
  <nav>
    <a href="/">Home</a>
    <a href="/collect">Collect Data</a>
    <a href="/visualize">Visualize Data</a>
    <a href="/analyze">Analyze Data</a>
  </nav>
  <div class="container">
    {{ content|safe }}
  </div>
  <footer>
    &copy; 2025 CryptoTrend Analyzer. All rights reserved.
  </footer>
</body>
</html>
"""

@app.route("/")
def index():
    # Updated homepage text with more detailed and professional information.
    content = """
    <h2>Welcome to CryptoTrend Analyzer!</h2>
    <p><strong>About Us:</strong> CryptoTrend Analyzer is a cutting-edge platform designed for cryptocurrency enthusiasts, investors, and analysts. Our platform leverages advanced data collection techniques, interactive visualizations, and comprehensive analytics to deliver actionable market insights in real-time.</p>
    <h3>Key Features:</h3>
    <ul>
      <li><strong>Automated Data Collection:</strong> We aggregate data from multiple sources including CoinGecko, Reddit, Yahoo Finance, Binance, and more.</li>
      <li><strong>Dynamic Visualizations:</strong> See real-time trends through interactive charts and graphs.</li>
      <li><strong>Comprehensive Analysis:</strong> Run detailed analyses to gain deep insights into market movements.</li>
      <li><strong>User-Friendly Interface:</strong> Designed with professionals and enthusiasts in mind for a seamless experience.</li>
    </ul>
    <p>Our mission is to empower you with the tools and insights needed to make informed decisions in the ever-evolving world of cryptocurrencies. Use the navigation above to begin collecting data, generating visualizations, or performing in-depth analyses.</p>
    """
    return render_template_string(base_template, title="Home - CryptoTrend Analyzer", content=content)

@app.route("/collect")
def collect():
    # Placeholder for data collection functionality.
    content = """
    <h2>Collect Data</h2>
    <p>Initiating data collection...</p>
    <p>Our system continuously gathers data from various crypto sources to ensure you have the latest information available.
    Please refer to the server logs for details on the data collection status.</p>
    """
    return render_template_string(base_template, title="Collect Data - CryptoTrend Analyzer", content=content)

@app.route("/visualize")
def visualize():
    # Create an in-memory sample visualization.
    data = {'x': [1, 2, 3, 4, 5], 'y': [5, 15, 8, 20, 12]}
    df = pd.DataFrame(data)
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x="x", y="y", marker="o", color="#4A90E2")
    plt.title("Sample Crypto Trend Visualization")
    plt.xlabel("Time Interval")
    plt.ylabel("Metric Value")
    img_buf = BytesIO()
    plt.savefig(img_buf, format="png", bbox_inches="tight")
    plt.close()
    img_buf.seek(0)
    encoded_img = base64.b64encode(img_buf.getvalue()).decode("utf-8")
    img_data = f"data:image/png;base64,{encoded_img}"
    
    content = f"""
    <h2>Interactive Visualization</h2>
    <p>This sample visualization demonstrates the dynamic trends observed in our crypto market data.
    The graph updates in real-time as new data is collected.</p>
    <div class="flex-container">
      <div class="flex-item">
        <img src="{img_data}" alt="Sample Visualization">
      </div>
    </div>
    """
    return render_template_string(base_template, title="Visualize Data - CryptoTrend Analyzer", content=content)

@app.route("/analyze")
def analyze():
    """
    Executes the external analysis script (analysis.py) and displays the generated visualizations.
    The analysis script must write its output images to config.VISUALIZATION_DIR.
    """
    script_path = os.path.join(project_root, "backend", "analysis.py")
    success = run_script(script_path, project_root)
    
    # Define the image file paths.
    trending_bar_path = os.path.join(config.VISUALIZATION_DIR, "trending_coins_bar.png")
    reddit_pie_path = os.path.join(config.VISUALIZATION_DIR, "trending_coins_reddit_pie.png")
    comprehensive_path = os.path.join(config.VISUALIZATION_DIR, "comprehensive_trends.png")
    
    # Attempt to embed the images.
    trending_bar_img = embed_image(trending_bar_path)
    reddit_pie_img = embed_image(reddit_pie_path)
    comprehensive_img = embed_image(comprehensive_path)
    
    if success and (trending_bar_img or reddit_pie_img or comprehensive_img):
        visuals_html = "<h2>Analysis Visualizations</h2><div class='flex-container'>"
        if trending_bar_img:
            visuals_html += f"""
            <div class='flex-item'>
              <h3>Trending Coins Bar Plot</h3>
              <img src="{trending_bar_img}" alt="Trending Coins Bar Plot">
            </div>
            """
        if reddit_pie_img:
            visuals_html += f"""
            <div class='flex-item'>
              <h3>Reddit Post Distribution</h3>
              <img src="{reddit_pie_img}" alt="Reddit Post Distribution">
            </div>
            """
        if comprehensive_img:
            visuals_html += f"""
            <div class='flex-item'>
              <h3>Comprehensive Trends</h3>
              <img src="{comprehensive_img}" alt="Comprehensive Trends Visualization">
            </div>
            """
        visuals_html += "</div><p>The above visualizations provide an in-depth look at current market trends and dynamics.</p>"
        content = visuals_html
    else:
        content = "<h2>Analysis Error</h2><p>There was an error executing the analysis script or generating visualizations. Please check the logs for details.</p>"
    
    return render_template_string(base_template, title="Analyze Data - CryptoTrend Analyzer", content=content)

def run_script(script_path, root_path):
    """
    Runs a Python script using subprocess.
    Returns True if the script executed successfully (exit code 0); otherwise, returns False.
    """
    if not os.path.exists(script_path):
        logging.error("Script not found: %s", script_path)
        return False

    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = root_path + (os.pathsep + current_pythonpath if current_pythonpath else "")

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=root_path,
            env=env
        )
    except Exception as e:
        logging.exception("Error running script %s: %s", script_path, e)
        return False

    if result.returncode != 0:
        logging.error("Script %s failed: %s", script_path, result.stderr)
        return False

    return True

if __name__ == "__main__":
    app.run(debug=True, port=8502)