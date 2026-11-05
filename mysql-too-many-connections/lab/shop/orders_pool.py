from sqlalchemy import create_engine, text
from db import URL
from payment import check_payment

pool = create_engine(URL, pool_size=20, max_overflow=0)   # at most 20 connections, reused


def place_order(seat):
    check_payment(seat)              # 1. wait for the payment, no connection held
    with pool.begin() as conn:       # 2. borrow a connection, save, give it back
        conn.execute(text("INSERT INTO orders (seat) VALUES (:s)"), {"s": seat})
