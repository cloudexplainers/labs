"""Driftwood Surf School's lessons API (P124 lab). nginx sends api.surf.test here (gunicorn on 127.0.0.1:5000).

GET  /lessons    this weekend's lessons
POST /bookings   {"lesson": id, "name": "..."}; needs the customer's sign-in cookie (session=...).
                 201 when booked, 409 when the lesson is full, 401 without the cookie.
The app knows nothing about CORS: every CORS header in this lab comes from nginx.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.sort_keys = False
LESSONS = [
    {"id": 1, "when": "Sat 9:00", "what": "Beginner group", "spaces": 0},
    {"id": 2, "when": "Sat 11:00", "what": "Beginner group", "spaces": 3},
    {"id": 3, "when": "Sun 10:00", "what": "Private lesson", "spaces": 1},
]


@app.get("/lessons")
def lessons():
    return jsonify(LESSONS)


@app.post("/bookings")
def book():
    if request.cookies.get("session") != "maya-7f3a":
        return jsonify(error="Please sign in to book"), 401
    data = request.get_json(silent=True) or {}
    lesson = next((l for l in LESSONS if l["id"] == data.get("lesson")), None)
    if lesson is None:
        return jsonify(error="No such lesson"), 404
    if lesson["spaces"] == 0:
        return jsonify(error=f"{lesson['when']} is full"), 409
    return jsonify(booked=f"{lesson['when']} {lesson['what']}", name=data.get("name", "")), 201
