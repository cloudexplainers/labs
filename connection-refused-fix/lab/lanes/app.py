# The bowling alley's lane booking app (Flask). The front desk asks it which lanes are free.
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/lanes")
def free_lanes():
    return jsonify(free=[3, 5, 8])


if __name__ == "__main__":
    app.run(port=5000)
