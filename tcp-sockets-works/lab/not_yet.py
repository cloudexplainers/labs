# The order screen started, but not taking orders yet: it listens and doesn't call accept() until Enter.
import socket

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind(("0.0.0.0", 9000))
srv.listen()
input("listening on port 9000, not accepting yet (Enter accepts one tablet)")
conn, addr = srv.accept()
print("accepted", addr, "- it had already sent:", conn.recv(1024).decode())
conn.close()
