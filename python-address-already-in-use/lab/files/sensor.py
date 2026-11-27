import random
import socket
import sys

bench = sys.argv[1]
reading = f"{bench}: {random.uniform(20.5, 22.5):.1f} C"
with socket.create_connection((sys.argv[2], 9000), timeout=3) as s:
    s.sendall(reading.encode() + b"\n")
    s.recv(10)
