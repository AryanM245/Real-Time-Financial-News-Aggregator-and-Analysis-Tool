import streamlit as st
import requests
import time
from requests.exceptions import ConnectionError

st.title("Real-Time Financial News Aggregator and Analysis Tool")

# FastAPI server URL
api_url = "http://app:8000"

# Fetch and display news
def fetch_news():
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(f"{api_url}/news")
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to fetch news. Status code: {response.status_code}")
                return []
        except ConnectionError:
            if attempt < max_retries - 1:
                st.warning(f"Connection failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                st.error("Failed to connect to the server after multiple attempts.")
                return []

news_data = fetch_news()

st.header("Latest Financial News")
for item in news_data:
    st.subheader(item["title"])
    st.write(item["summary"])
    st.write(f"Source: {item['source']}")
    st.write(f"[Read more]({item['url']})")

# Add a query input and button
query = st.text_input("Enter your query about financial news:")
if st.button("Submit Query"):
    try:
        response = requests.get(f"{api_url}/query", params={"query": query})
        if response.status_code == 200:
            result = response.json()
            st.subheader("Query Result")
            st.write(result["query_result"])
            st.subheader("Analysis")
            st.write(result["analysis"])
        else:
            st.error(f"Failed to process query. Status code: {response.status_code}")
    except ConnectionError:
        st.error("Failed to connect to the server. Please try again later.")