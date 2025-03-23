FROM python:3.12-slim
WORKDIR /app

ENV PYTHONPATH .

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev libmagic-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./start.sh
CMD ["./start.sh"]
