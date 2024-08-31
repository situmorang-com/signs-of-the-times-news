import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import sqlite3

# Fetch Relevant Articles
def fetch_relevant_articles():
    conn = sqlite3.connect('news.db')
    df = pd.read_sql_query("SELECT * FROM articles WHERE relevance_score > 2", conn)
    conn.close()
    return df

# Send Email Alerts
def send_email_alert(subject, body, to_email):
    from_email = 'your_email@example.com'
    password = 'your_password'
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Generate Weekly Summary
def generate_weekly_summary():
    articles_df = fetch_relevant_articles()
    
    summary = "Weekly Summary of Signs of the Times:\n\n"
    
    for topic, group in articles_df.groupby('top_topic'):
        summary += f"{topic}:\n"
        for _, article in group.iterrows():
            summary += f"- {article['title']} (Relevance: {article['relevance_score']:.2f})\n"
            summary += f"  {article['url']}\n\n"
        summary += "\n"
    
    return summary

# Main Function
if __name__ == "__main__":
    summary = generate_weekly_summary()
    send_email_alert("Weekly Summary of Relevant News", summary, "recipient@example.com")
    print("Alert sent.")