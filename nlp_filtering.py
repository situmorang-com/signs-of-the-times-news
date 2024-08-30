import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from transformers import pipeline
import sqlite3

# Load SpaCy NLP Model
nlp = spacy.load('en_core_web_sm')

# Function to Preprocess Text
def preprocess_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

# Function for Topic Modeling
def topic_modeling(texts, n_topics=5):
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    return lda, vectorizer

# Function for Sentiment Analysis
def sentiment_analysis(texts):
    sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
    return [sentiment_analyzer(text)[0]['label'] for text in texts]

# Fetch Articles from Database
def fetch_articles():
    conn = sqlite3.connect('news.db')
    df = pd.read_sql_query("SELECT * FROM articles", conn)
    conn.close()
    return df

# Function for Relevance Scoring
def relevance_scoring(df, keywords, lda_model, vectorizer):
    df['preprocessed'] = df['content'].apply(preprocess_text)
    df['keyword_score'] = df['content'].apply(lambda x: sum(1 for word in keywords if word in x))
    df['topic_score'] = df['preprocessed'].apply(lambda x: lda_model.transform(vectorizer.transform([x]))[0].max())
    df['sentiment'] = sentiment_analysis(df['content'])
    df['sentiment_score'] = df['sentiment'].apply(lambda x: 1 if x == 'POSITIVE' else -1)
    df['relevance_score'] = df['keyword_score'] + df['topic_score'] + df['sentiment_score']
    return df

# Update Relevance Scores in the Database
def update_relevance_score(df):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    for index, row in df.iterrows():
        c.execute("UPDATE articles SET relevance_score = ? WHERE id = ?", (row['relevance_score'], row['id']))
    conn.commit()
    conn.close()

# Main function to run NLP filtering
def run_nlp_filtering():
    articles_df = fetch_articles()
    keywords = ["Sunday law", "religious liberty", "Sabbath observance", "climate change laws"]
    lda_model, vectorizer = topic_modeling(articles_df['content'])
    scored_df = relevance_scoring(articles_df, keywords, lda_model, vectorizer)
    update_relevance_score(scored_df)
    print("Relevance scores have been updated in the database.")

# Make callable from outside
if __name__ == "__main__":
    run_nlp_filtering()
