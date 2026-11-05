"""Kettle shop: talk to the payment service."""
import os
import urllib.request

API = "http://payments"
KEY = os.environ["PAYMENTS_API_KEY"]   # read from .env when the shop starts


def balance():
    req = urllib.request.Request(API + "/v1/balance", headers={"Authorization": f"Bearer {KEY}"})
    return urllib.request.urlopen(req).read().decode()
