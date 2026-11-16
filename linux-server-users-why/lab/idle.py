"""Opens N connections to the market's page, loads it once on each, then leaves them all open and idle,
like N people with the page open in a browser tab. Usage: python3 idle.py N SECONDS"""
import resource
import socket
import sys
import time

n, hold = int(sys.argv[1]), int(sys.argv[2])
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))   # one file handle per connection
socks = []
for _ in range(n):
    s = socket.create_connection(("market", 80))
    s.sendall(b"GET / HTTP/1.1\r\nHost: market\r\n\r\n")
    data = b""
    while b"</html>" not in data:
        data += s.recv(65536)
    socks.append(s)
print(f"{len(socks)} connections open, page loaded on each, now idle for {hold} s")
sys.stdout.flush()
time.sleep(hold)
