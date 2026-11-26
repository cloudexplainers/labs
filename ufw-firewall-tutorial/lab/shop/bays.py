"""The shop's bay screens page: which car is in which bay. Meant for the shop's own screens only."""
from flask import Flask

app = Flask(__name__)
BAYS = [("Bay 1", "Corolla", "4 winter tires", "Dave"), ("Bay 2", "Transit van", "puncture repair", "Beth"),
        ("Bay 3", "Civic", "wheel balance", "Dave")]


@app.get("/")
def bays():
    return "\n".join(f"{b}: {car}, {job} ({who})" for b, car, job, who in BAYS) + "\n"


app.run(host="0.0.0.0", port=5000)
