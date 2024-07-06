import pathway as pw
from fastapi import FastAPI
import uvicorn
import asyncio
from data_ingestion import fetch_and_process_news
from indexing import query_news, initialize_index
import logging

app = FastAPI()
pw.set_license_key("demo-license-key-with-telemetry")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store processed news
processed_news = []

async def update_news_and_index():
    global processed_news
    while True:
        try:
            new_news = fetch_and_process_news()
            if new_news != processed_news:
                processed_news = new_news
                await initialize_index(processed_news)
                logger.info("News updated and index reinitialized")
            else:
                logger.info("No new news to update")
        except Exception as e:
            logger.error(f"Error updating news and index: {e}")
        await asyncio.sleep(3600)  # Update every hour

@app.get("/news")
async def get_news():
    logger.info("Fetching news...")
    return processed_news

@app.get("/query")
async def get_query(query: str):
    logger.info(f"Received query: {query}")
    result = await query_news(query, processed_news)
    logger.info(f"Query result: {result}")
    return {"query": query, "result": result}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    async def run_pathway():
        await pw.udf_async()

    async def main():
        logger.info("Starting server...")
        global processed_news
        processed_news = fetch_and_process_news()
        pathway_task = asyncio.create_task(run_pathway())
        news_update_task = asyncio.create_task(update_news_and_index())
        
        # Initialize index with initial news data
        await initialize_index(processed_news)
        
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await asyncio.gather(news_update_task, server.serve(), pathway_task)
        logger.info("Server started successfully.")
    
    asyncio.run(main())
