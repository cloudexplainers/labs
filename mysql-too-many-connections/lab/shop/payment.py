"""Stands in for the payment provider: every check takes about three seconds."""
import time


def check_payment(seat):
    time.sleep(3)
