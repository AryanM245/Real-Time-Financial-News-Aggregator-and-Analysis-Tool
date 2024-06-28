FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .
COPY .env .

# Download NLTK data
COPY download_nltk_data.py .
RUN python download_nltk_data.py

CMD ["python", "main.py"]
