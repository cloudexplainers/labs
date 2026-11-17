from flask import Flask

app = Flask(__name__)
CLASSES = ["07:00  Sunrise flow", "12:15  Lunch stretch", "18:30  Evening yin (new teacher)"]


@app.route("/")
def home():
    items = "".join(f"<li>{c}</li>" for c in CLASSES)
    return f"<h1>Willow Yoga: today's classes</h1><ul>{items}</ul>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
