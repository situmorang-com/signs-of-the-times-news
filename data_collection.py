import requests
import sqlite3
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get API key from environment variable
api_key = os.getenv('MY_API_KEY')

# Ensure API key is loaded
if not api_key:
    logging.error("API key is missing. Please set the MY_API_KEY environment variable.")
    raise ValueError("API key is missing. Check your .env file or environment variable settings.")

# Initialize Database
def init_db():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (
                 id INTEGER PRIMARY KEY,
                 title TEXT,
                 content TEXT,
                 url TEXT,
                 publication_date TEXT,
                 relevance_score REAL
                 )''')
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

# Fetch News from News API
def fetch_news_from_api(keyword):
    try:
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}"
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise an HTTPError for bad responses
        articles = response.json().get('articles', [])
        logging.info(f"Fetched {len(articles)} articles for keyword '{keyword}'.")
        return [{'title': a['title'], 'content': a['content'], 'url': a['url'], 'publication_date': a['publishedAt']} for a in articles]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return []

# Save Articles to Database
def save_articles(articles):
    if not articles:
        logging.info("No articles to save.")
        return
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    for article in articles:
        c.execute("INSERT INTO articles (title, content, url, publication_date) VALUES (?, ?, ?, ?)",
                  (article['title'], article['content'], article['url'], article['publication_date']))
    conn.commit()
    conn.close()
    logging.info(f"Saved {len(articles)} articles to the database.")

# Main function to run data collection with a dynamic keyword
def run_data_collection(keyword):
    if not keyword:
        logging.error("Keyword is missing. Please provide a valid keyword for data collection.")
        return

    init_db()
    articles = fetch_news_from_api(keyword)  # Use the provided keyword
    save_articles(articles)
    logging.info("Data collection completed.")

# Make callable from outside
if __name__ == "__main__":
    # Prompt for keyword if not provided as a script argument
    keyword = input("Enter keyword for news data collection: ")
    run_data_collection(keyword)
