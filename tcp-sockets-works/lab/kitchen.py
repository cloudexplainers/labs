# The kitchen's order screen: waits for the tablets on port 9000 and prints every order as a ticket.
import socket
import threading
import time


def serve(conn, addr):
    print("tablet connected from", addr)
    while True:
        time.sleep(1)                            # the screen refreshes once a second
        data = conn.recv(1024)                   # whatever has arrived, up to 1024 bytes
        if not data:                             # b"" means the tablet hung up
            break
        print("TICKET:", data.decode())
    print("tablet hung up:", addr)
    conn.close()


srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 1. a TCP socket
srv.bind(("0.0.0.0", 9000))                               # 2. an address and a port
srv.listen()                                              # 3. ready for calls
print("kitchen screen: listening on port 9000")
try:
    while True:
        conn, addr = srv.accept()                         # 4. a new socket for each tablet
        threading.Thread(target=serve, args=(conn, addr), daemon=True).start()
except KeyboardInterrupt:
    print("kitchen screen closing")
