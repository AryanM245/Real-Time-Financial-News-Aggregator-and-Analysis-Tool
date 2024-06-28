from typing import List
import openai
from llama_index.legacy import VectorStoreIndex, Document
from llama_index.embeddings.openai import OpenAIEmbedding
import pathway as pw
from llama_index.core import Settings
from dotenv import load_dotenv
import os
import time

pw.set_license_key("demo-license-key-with-telemetry")
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

class RateLimitedOpenAIEmbedding:
    def __init__(self, api_key: str):
        self.embed_model = OpenAIEmbedding(api_key=api_key)
        self.last_request_time = 0
        self.request_interval = 1  # Minimum time between requests in seconds
        self.max_retries = 5
        self.retry_delay = 60 

    def get_text_embedding(self, text: str) -> List[float]:
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.request_interval:
            time.sleep(self.request_interval - time_since_last_request)
        
        for retry in range(self.max_retries):
            try:
                result = self.embed_model.get_text_embedding(text)
                self.last_request_time = time.time()
                return result
            except openai.RateLimitError:
                if retry < self.max_retries - 1:
                    print(f"Rate limit exceeded. Waiting for {self.retry_delay} seconds before retrying.")
                    time.sleep(self.retry_delay)
                else:
                    raise

    def get_text_embedding_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.get_text_embedding(text) for text in texts]

embed_model = RateLimitedOpenAIEmbedding(api_key=OPENAI_API_KEY)

def index_documents(news_items, batch_size=10):
    all_documents = [Document(text=item['summary'], metadata={'title': item['title']}) for item in news_items]
    index = None
    
    for i in range(0, len(all_documents), batch_size):
        batch = all_documents[i:i+batch_size]
        if index is None:
            index = VectorStoreIndex.from_documents(batch, embed_model=embed_model)
        else:
            index.insert_nodes(batch)
        
        time.sleep(1)  # Add a small delay between batches
    
    return index

def query_index(index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return str(response)

# Import processed_news
from data_ingestion import processed_news

# Create a single index for all news items
index = index_documents(processed_news)

# Create a Pathway object for the index
indexed_news = pw.io.memory({0: index})