import openai
from llama_index.legacy import VectorStoreIndex, Document
from llama_index.embeddings.openai import OpenAIEmbedding
import pathway as pw
from dotenv import load_dotenv
import os
import time
import asyncio
import logging
from tenacity import retry, wait_random_exponential, stop_after_attempt

pw.set_license_key("demo-license-key-with-telemetry")
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

logger = logging.getLogger(__name__)

class RateLimitedOpenAIEmbedding:
    def __init__(self, api_key: str):
        self.embed_model = OpenAIEmbedding(api_key=api_key)
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    async def get_text_embedding(self, text: str):
        try:
            return self.embed_model.get_text_embedding(text)
        except openai.RateLimitError:
            logger.warning("Rate limit exceeded. Retrying...")
            raise

    async def get_text_embedding_batch(self, texts):
        return [await self.get_text_embedding(text) for text in texts]

embed_model = RateLimitedOpenAIEmbedding(api_key=OPENAI_API_KEY)

async def index_documents(news_items, batch_size=5):
    all_documents = [Document(text=item['summary'], metadata={'title': item['title']}) for item in news_items]
    index = None
    
    for i in range(0, len(all_documents), batch_size):
        batch = all_documents[i:i+batch_size]
        if index is None:
            index = await VectorStoreIndex.from_documents(batch, embed_model=embed_model)
        else:
            await index.insert_nodes(batch)
        
        await asyncio.sleep(1)  # Add a small delay between batches
    
    return index

async def query_index(index, query):
    query_engine = index.as_query_engine()
    response = await asyncio.to_thread(query_engine.query, query)
    return str(response)

# Global variable to store the index
global_index = None

async def initialize_index(news_data):
    global global_index
    global_index = await index_documents(news_data)

async def get_or_create_index(news_data):
    global global_index
    if global_index is None:
        await initialize_index(news_data)
    return global_index

async def query_news(query: str, news_data):
    try:
        logger.info(f"Received query: {query}")
        index = await get_or_create_index(news_data)
        logger.info("Index initialized. Querying index...")
        response = await query_index(index, query)
        logger.info(f"Query response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error querying news: {e}")
        return str(e)
