FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/local/share/nltk_data

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        imagemagick \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader \
    -d /usr/local/share/nltk_data \
    punkt \
    punkt_tab

COPY . .

CMD ["python", "main.py"]