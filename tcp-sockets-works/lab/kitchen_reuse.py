# The kitchen's order screen: waits for the tablets on port 9000 and prints every order as a ticket.
import socket
import threading


def serve(conn, addr):
    print("tablet connected from", addr)
    for line in conn.makefile(encoding="utf-8"):  # one order per line, however it arrived
        print("TICKET:", line.rstrip("\n"))
    print("tablet hung up:", addr)
    conn.close()


srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 1. a TCP socket
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # reuse the port right after a restart
srv.bind(("0.0.0.0", 9000))                               # 2. an address and a port
srv.listen()                                              # 3. ready for calls
print("kitchen screen: listening on port 9000")
try:
    while True:
        conn, addr = srv.accept()                         # 4. a new socket for each tablet
        threading.Thread(target=serve, args=(conn, addr), daemon=True).start()
except KeyboardInterrupt:
    print("kitchen screen closing")
