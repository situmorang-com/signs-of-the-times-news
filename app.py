from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import pandas as pd
from data_collection import run_data_collection
from nlp_filtering import run_nlp_filtering, adventist_topic_modeling, categorize_articles

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for using Flask's flash messages

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

@app.route('/collect-data', methods=['POST'])
def collect_data():
    keyword = request.form.get('keyword')  # Get the keyword from the form input
    if keyword:
        run_data_collection(keyword)  # Run data collection with the provided keyword
        flash(f"Data collection completed for keyword: '{keyword}'", "success")
    else:
        flash("Please enter a keyword to collect news.", "danger")
    return redirect(url_for('home'))

@app.route('/filter-data')
def filter_data():
    run_nlp_filtering()
    flash("Data filtering and scoring completed.", "success")
    return redirect(url_for('home'))

@app.route('/topics')
def topics():
    conn = sqlite3.connect('news.db')
    df = pd.read_sql_query("SELECT * FROM articles WHERE relevance_score > 2", conn)
    conn.close()
    
    articles_by_topic = df.groupby('top_topic').apply(lambda x: x.to_dict('records')).to_dict()
    
    return render_template('topics.html', articles_by_topic=articles_by_topic)

if __name__ == '__main__':
    app.run(debug=True, port=5001)