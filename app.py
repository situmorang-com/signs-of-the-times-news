from flask import Flask, render_template, redirect, url_for
import sqlite3
from data_collection import run_data_collection
from nlp_filtering import run_nlp_filtering

app = Flask(__name__)

# Fetch Articles from Database
def fetch_articles():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, content, url FROM articles WHERE relevance_score > 2")
    articles = cursor.fetchall()
    conn.close()
    return articles

@app.route('/')
def home():
    articles = fetch_articles()
    return render_template('index.html', articles=articles)

@app.route('/collect-data')
def collect_data():
    run_data_collection()
    return redirect(url_for('home'))

@app.route('/filter-data')
def filter_data():
    run_nlp_filtering()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False, port=5001)
