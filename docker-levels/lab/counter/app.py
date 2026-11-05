from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host="redis", port=6379)


@app.get("/")
def home():
    count = redis.incr("visits")
    return f"Visits so far: {count}\n"
