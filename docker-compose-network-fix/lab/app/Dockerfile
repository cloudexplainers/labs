# Ana's tea shop app image (teashop:1): a tiny web page and a nightly report, both reading PostgreSQL.
FROM python:3.13-slim
RUN pip install --no-cache-dir "psycopg[binary]==3.2.12"
WORKDIR /app
COPY web.py report.py ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "web.py"]
