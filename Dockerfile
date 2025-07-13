FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget cron && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY enrich.py .
COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

RUN echo "0 2 * * 0 /app/entrypoint.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/geoip-cron
RUN chmod 0644 /etc/cron.d/geoip-cron && crontab /etc/cron.d/geoip-cron

CMD ["cron", "-f"]
