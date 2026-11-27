from flask import Flask

app = Flask(__name__)
BENCHES = {"bench 1": "21.4 C", "bench 2": "22.1 C", "bench 3": "20.8 C"}


@app.route("/")
def temperatures():
    rows = "".join(f"<li>{bench}: {temp}</li>" for bench, temp in BENCHES.items())
    return f"<h1>Greenhouse</h1><ul>{rows}</ul>"


if __name__ == "__main__":
    app.run(port=5000)
