import pathway as pw
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
def analyze_news(news):
    # Alpha Vantage already provides sentiment, so we'll use that
    return {
        'sentiment_score': float(news['overall_sentiment_score']),
        'sentiment_label': news['overall_sentiment_label'],
        'category': news['category_within_source'],
        # You can add more analysis here
    }

def process_news_item(news_item):
    analysis_results = analyze_news(news_item)
    return pw.Record(
        original_news=news_item,
        analysis=analysis_results
    )

# Assuming you have a news stream from data_ingestion.py
from data_ingestion import processed_news

# Apply the analysis to the news stream
analyzed_news = processed_news.map(process_news_item)

# Aggregate sentiment over time
sentiment_over_time = analyzed_news.groupby(
    pw.this.original_news.time_published.dt.floor("1h")
).reduce(
    time=pw.reducers.first(pw.this.original_news.time_published),
    avg_sentiment=pw.reducers.mean(pw.this.analysis.sentiment_score)
)

# Group news by category
news_by_category = analyzed_news.groupby(
    pw.this.analysis.category
).reduce(
    category=pw.this.key,
    count=pw.reducers.count(),
    avg_sentiment=pw.reducers.mean(pw.this.analysis.sentiment_score)
)