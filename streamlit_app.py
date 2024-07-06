import streamlit as st
import requests
import time
from requests.exceptions import RequestException
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.title("Real-Time Financial News Aggregator and Analysis Tool")

# FastAPI server URL
api_url = "http://app:8000"

# Fetch and display news
def fetch_news():
    max_retries = 5
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            logger.debug(f"Attempting to connect to {api_url}/news")
            response = requests.get(f"{api_url}/news")
            logger.debug(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch news. Status code: {response.status_code}")
                st.error(f"Failed to fetch news. Status code: {response.status_code}")
                return []
        except RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.warning(f"Retrying in {retry_delay} seconds...")
                st.warning(f"Connection failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Failed to connect to the server after multiple attempts.")
                st.error("Failed to connect to the server after multiple attempts.")
                return []

news_data = fetch_news()

st.header("Latest Financial News")
if news_data:
    for item in news_data:
        st.subheader(item["title"])
        st.write(item["summary"])
        st.write(f"Source: {item['source']}")
        st.write(f"[Read more]({item['url']})")
else:
    st.write("No news available at the moment.")

# Add a query input and button
query = st.text_input("Enter your query about financial news:")
if st.button("Submit Query"):
    try:
        logger.debug(f"Submitting query: {query}")
        response = requests.get(f"{api_url}/query", params={"query": query})
        logger.debug(f"Query response status code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            st.subheader("Query Result")
            st.write(result.get("result", "No result available"))
        else:
            logger.error(f"Failed to process query. Status code: {response.status_code}")
            st.error(f"Failed to process query. Status code: {response.status_code}")
    except RequestException as e:
        logger.error(f"Failed to connect to the server: {str(e)}")
        st.error("Failed to connect to the server. Please try again later.")
