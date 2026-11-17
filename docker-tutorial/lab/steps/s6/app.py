import os

import psycopg
from flask import Flask

app = Flask(__name__)
DB = os.environ["DATABASE_URL"]


@app.route("/")
def home():
    with psycopg.connect(DB) as conn:
        rows = conn.execute("SELECT start, name FROM classes ORDER BY start").fetchall()
    items = "".join(f"<li>{start}  {name}</li>" for start, name in rows)
    return f"<h1>Willow Yoga: today's classes</h1><ul>{items}</ul>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
