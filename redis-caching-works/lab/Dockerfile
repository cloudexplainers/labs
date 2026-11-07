FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends redis-tools procps && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir redis==6.4.0 "psycopg[binary]==3.2.10" \
 && useradd -m -s /bin/bash ana
USER ana
WORKDIR /home/ana/shop
