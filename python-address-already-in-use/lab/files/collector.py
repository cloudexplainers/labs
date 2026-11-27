import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 9000))
server.listen()
print("collector listening on port 9000", flush=True)
try:
    while True:
        conn, addr = server.accept()
        reading = conn.recv(100).decode().strip()
        print(reading, flush=True)
        conn.sendall(b"ok\n")
        conn.close()
except KeyboardInterrupt:
    print("collector stopped")
finally:
    server.close()
