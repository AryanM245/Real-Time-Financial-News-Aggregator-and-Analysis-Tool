import requests
from datetime import datetime
import time
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def fetch_news():
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('feed', [])

def process_news(news_data):
    processed_news = []
    for article in news_data:
        processed_news.append({
            'title': article.get('title', ''),
            'url': article.get('url', ''),
            'time_published': article.get('time_published', ''),
            'authors': article.get('authors', ''),
            'summary': article.get('summary', ''),
            'source': article.get('source', ''),
            'category_within_source': article.get('category_within_source', ''),
            'overall_sentiment_score': article.get('overall_sentiment_score', ''),
            'overall_sentiment_label': article.get('overall_sentiment_label', '')
        })
    return processed_news

def fetch_and_process_news():
    news_data = fetch_news()
    return process_news(news_data)
