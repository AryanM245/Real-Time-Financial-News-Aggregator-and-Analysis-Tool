FROM python:3.11

WORKDIR /app


RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY download_nltk_data.py .
RUN python download_nltk_data.py

# Copy application filesCOPY *.py .
COPY .env .


CMD ["python", "main.py"]
