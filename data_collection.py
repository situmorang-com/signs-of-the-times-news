import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('MY_API_KEY')
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

# Fetch News from News API
def fetch_news_from_api(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return [{'title': a['title'], 'content': a['content'], 'url': a['url'], 'publication_date': a['publishedAt']} for a in articles]
    else:
        print(f"Error fetching data from API: {response.status_code}")
        return []

# Save Articles to Database
def save_articles(articles):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    for article in articles:
        c.execute("INSERT INTO articles (title, content, url, publication_date) VALUES (?, ?, ?, ?)",
                  (article['title'], article['content'], article['url'], article['publication_date']))
    conn.commit()
    conn.close()

# Main function to run data collection
def run_data_collection():
    init_db()
    articles = fetch_news_from_api('Sunday law')  # Example query
    save_articles(articles)
    print("Data collection completed.")

# Make callable from outside
if __name__ == "__main__":
    run_data_collection()
