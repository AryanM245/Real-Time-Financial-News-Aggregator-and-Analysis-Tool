import pathway as pw
from fastapi import FastAPI
import uvicorn
import asyncio
from data_ingestion import processed_news
from llm_integration import analyze_news
from indexing import query_index, index_documents

app = FastAPI()
pw.set_license_key("demo-license-key-with-telemetry")

# Create a single index for all news items
index = index_documents(processed_news)

# Create a Pathway object for the index
indexed_news = pw.io.memory({0: index})

@app.get("/news")
async def get_news():
    return processed_news

@app.get("/query")
async def process_query(query: str):
    result = query_index(indexed_news, query)
    analysis = analyze_news(processed_news, query)
    return {"query_result": result, "analysis": analysis}

if __name__ == "__main__":
    async def run_pathway():
        await pw.udf_async()

    async def main():
        pathway_task = asyncio.create_task(run_pathway())
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()
        await pathway_task
    
    asyncio.run(main())
