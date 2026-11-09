FROM python:3.13-slim
RUN pip install --no-cache-dir "psycopg[binary]==3.2.10"
COPY app.py /app.py
CMD ["python", "/app.py"]
