import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from transformers import pipeline
import sqlite3

# Load SpaCy NLP Model
nlp = spacy.load('en_core_web_sm')

# Refined Keywords
keywords = [
    "Sunday law", "religious liberty", "Sabbath observance", "climate change laws",
    "mark of the beast", "end times", "prophecy fulfillment", "church and state",
    "religious persecution", "Vatican", "papacy", "ecumenical movement",
    "natural disasters", "moral decline", "religious legislation",
    "global crisis", "world order", "religious freedom", "false worship",
    "Bible prophecy", "three angels' messages", "latter rain", "loud cry",
    "time of trouble", "National Sunday Law", "blue laws", "day of rest"
]

# Function to Preprocess Text
def preprocess_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

# Function for Adventist-specific Topic Modeling
def adventist_topic_modeling(texts, n_topics=7):
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    
    # Define Adventist-specific topics
    adventist_topics = [
        "Sunday Law and Religious Liberty",
        "End-Time Prophecy and World Events",
        "Church and State Relations",
        "Natural Disasters and Climate Change",
        "Moral Decline and Social Issues",
        "Ecumenical Movement and False Unity",
        "Preparation for Christ's Return"
    ]
    
    # Assign topic names to the LDA model
    topic_names = {i: name for i, name in enumerate(adventist_topics)}
    
    return lda, vectorizer, topic_names

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

# Function for Improved Relevance Scoring
def relevance_scoring(df, keywords, lda_model, vectorizer):
    df['preprocessed'] = df['content'].apply(preprocess_text)
    df['keyword_score'] = df['content'].apply(lambda x: sum(3 for word in keywords if word.lower() in x.lower()))
    df['topic_score'] = df['preprocessed'].apply(lambda x: lda_model.transform(vectorizer.transform([x]))[0].max() * 2)
    df['sentiment'] = sentiment_analysis(df['content'])
    df['sentiment_score'] = df['sentiment'].apply(lambda x: 1 if x == 'POSITIVE' else -1)
    df['relevance_score'] = df['keyword_score'] + df['topic_score'] + df['sentiment_score']
    return df

# Categorize Articles
def categorize_articles(df, lda_model, vectorizer, topic_names):
    df['top_topic'] = df['preprocessed'].apply(
        lambda x: topic_names[lda_model.transform(vectorizer.transform([x]))[0].argmax()]
    )
    return df

# Update Relevance Scores and Topics in the Database
def update_database(df):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    for index, row in df.iterrows():
        c.execute("UPDATE articles SET relevance_score = ?, top_topic = ? WHERE id = ?", 
                  (row['relevance_score'], row['top_topic'], row['id']))
    conn.commit()
    conn.close()

# Main function to run NLP filtering
def run_nlp_filtering():
    articles_df = fetch_articles()
    lda_model, vectorizer, topic_names = adventist_topic_modeling(articles_df['content'])
    scored_df = relevance_scoring(articles_df, keywords, lda_model, vectorizer)
    categorized_df = categorize_articles(scored_df, lda_model, vectorizer, topic_names)
    update_database(categorized_df)
    print("Relevance scores and topics have been updated in the database.")

# Make callable from outside
if __name__ == "__main__":
    run_nlp_filtering()