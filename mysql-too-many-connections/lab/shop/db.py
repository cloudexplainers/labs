"""Where the ticket shop's database is. The password comes from the environment, never from the code."""
import os

DB = dict(host="db", user="shop", password=os.environ["DB_PASSWORD"], database="tickets")
URL = f"mysql+pymysql://shop:{os.environ['DB_PASSWORD']}@db/tickets"
