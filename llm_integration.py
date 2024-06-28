from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import time
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RateLimitedOpenAI(OpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_request_time = 0
        self.request_interval = 1  # Minimum time between requests in seconds
        self.max_retries = 5
        self.retry_delay = 60  # Delay in seconds before retrying after a rate limit error

    def generate(self, prompts, stop=None):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.request_interval:
            time.sleep(self.request_interval - time_since_last_request)
        
        for retry in range(self.max_retries):
            try:
                result = super().generate(prompts, stop)
                self.last_request_time = time.time()
                return result
            except openai.error.RateLimitError:
                if retry < self.max_retries - 1:
                    print(f"Rate limit exceeded. Waiting for {self.retry_delay} seconds before retrying.")
                    time.sleep(self.retry_delay)
                else:
                    raise

llm = RateLimitedOpenAI(temperature=0.7, api_key=OPENAI_API_KEY)

prompt = PromptTemplate(
    input_variables=["news", "query"],
    template="Based on the following financial news: {news}\n\nAnswer the query: {query}"
)

chain = LLMChain(llm=llm, prompt=prompt)

def analyze_news(news, query):
    return chain.run(news=news, query=query)
