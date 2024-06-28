# Real-Time Financial News Aggregator and Analysis Tool

## Project Description

The Real-Time Financial News Aggregator and Analysis Tool is designed to provide users with up-to-date news, insights, and analysis on financial markets using a Retrieval-Augmented Generation (RAG) approach. This tool educates users about the latest trends in various industries by aggregating financial news and providing insightful analyses.

## Components

### Pathway
Pathway is used for streaming data processing and handling the pipeline of ingesting, processing, and indexing financial news data in real-time.

### LangChain
LangChain is utilized for building chains of logic to process data. In this project, it handles the logical flow for querying the language model and structuring prompts for analysis.

### Llama-Index
Llama-Index (formerly known as GPT Index) is employed to build a vector store index for efficient querying of financial news data. It leverages embeddings to enable semantic search capabilities.

### OpenAI
OpenAI provides the language model used for generating responses and analyses. The project uses the OpenAI API for generating insights based on financial news data.

### Alpha Vantage API
Alpha Vantage API is used for retrieving real-time financial news and market data. This API provides the raw news data that is processed and analyzed by the tool.

### Streamlit UI
Streamlit is used to create an interactive user interface, allowing users to input queries, view aggregated news, and receive analysis results in a user-friendly manner.

## Features
- Aggregates real-time financial news
- Provides insightful analysis based on user queries
- Interactive UI for querying and viewing results
- Handles rate limits and retries for API calls

## Setup and Usage

### Prerequisites

- Docker
- Docker Compose
- Python 3.11

### Steps to Set Up and Run the Project

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/financial-news-aggregator.git
   cd financial-news-aggregator
2. **Create and Configure the .env File**
    Create a .env file in the project root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
3. **Build and Run the Docker Containers**
    Build and run the containers using Docker Compose:
    ```bash
    docker-compose up --build
4. **Access the Streamlit UI**
    Once the containers are up and running, you can access the Streamlit UI at:
    ```arduino
    http://localhost:8501
### Project Structure

- data_ingestion.py: Script for ingesting and processing financial news data.
- indexing.py: Script for indexing the processed news data using Llama-Index.
- llm_integration.py: Script for integrating with OpenAI's language model and handling rate limits.
- main.py: Main FastAPI application that serves the news data and handles queries.
- streamlit_app.py: Streamlit application for the user interface.
- download_nltk_data.py: Script to download necessary NLTK data packages.
- Dockerfile: Dockerfile for setting up the project environment.
- docker-compose.yml: Docker Compose configuration file.

### Additional Configuration

    If you need to modify the behavior of the rate-limiting logic or other parameters, you can do so in the respective scripts (llm_integration.py, indexing.py).

### Troubleshooting
    If you encounter any issues during setup or usage, consider the following:

- Ensure your API keys are correct and have sufficient quota.
- Check the Docker logs for any error messages.
- Verify that the required Python packages are installed correctly.
- Try modifying the behavior of the rate limiting logic (in llm_integration.py).

### License
This project is licensed under the MIT License. See the license file.

### Acknowledgements
- OpenAI
- LangChain
- Llama-Index
- Pathway
- Streamlit
- Alpha Vantage
