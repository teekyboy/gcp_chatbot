FROM --platform=linux/amd64 python:3.10.11-buster

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY . /app

ENV PORT=8080

EXPOSE $PORT

CMD ["sh", "-c", "streamlit run --server.port $PORT personal_bot/frontend.py"]
