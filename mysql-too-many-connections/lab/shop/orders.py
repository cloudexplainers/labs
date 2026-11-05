import pymysql
from db import DB
from payment import check_payment


def place_order(seat):
    conn = pymysql.connect(**DB)     # 1. open a new connection
    check_payment(seat)              # 2. wait about 3 s for the payment
    with conn.cursor() as cur:       # 3. save the order
        cur.execute("INSERT INTO orders (seat) VALUES (%s)", (seat,))
    conn.commit()
    conn.close()
