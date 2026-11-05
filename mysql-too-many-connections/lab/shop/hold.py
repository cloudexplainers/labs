"""Off-screen measuring tool: open N idle connections and keep them until killed."""
import sys
import time
import pymysql
from db import DB

conns = [pymysql.connect(**DB) for _ in range(int(sys.argv[1]))]
print(f"holding {len(conns)}", flush=True)
time.sleep(10**6)
