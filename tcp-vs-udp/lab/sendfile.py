#!/usr/bin/env python3
"""Send a file over TCP or UDP, the same way for both: in pieces of 1,400 bytes, one after another.

  python3 sendfile.py receive tcp|udp           (on the server: saves what arrives as photo.jpg)
  python3 sendfile.py send tcp|udp FILE HOST    (on the laptop)

TCP hands each piece to the operating system, which numbers, acknowledges and resends.
UDP sends each piece as one datagram, with nothing on top: what is lost stays lost.
"""
import socket, sys, time

PORT, PIECE = 7000, 1400


def send(proto, path, host):
    data = open(path, "rb").read()
    pieces = [data[i:i + PIECE] for i in range(0, len(data), PIECE)]
    if proto == "tcp":
        s = socket.create_connection((host, PORT))
        for p in pieces:
            s.sendall(p)
        s.shutdown(socket.SHUT_WR)
        s.recv(1)                      # wait until the receiver has everything
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = (socket.gethostbyname(host), PORT)
        for p in pieces:
            s.sendto(p, addr)
            time.sleep(0.001)          # one piece a millisecond, so no queue overflows on the way
    print(f"sent {len(data):,} bytes in {len(pieces):,} pieces over {proto.upper()}")


def receive(proto):
    got, n = bytearray(), 0
    if proto == "tcp":
        srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("", PORT)); srv.listen(1)
        conn, _ = srv.accept()
        while chunk := conn.recv(65536):
            got += chunk
        conn.sendall(b"k"); conn.close()
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.bind(("", PORT))
        while True:
            try:
                got += s.recv(2048); n += 1
            except socket.timeout:
                break
            s.settimeout(2.0)          # done once nothing arrives for 2 s
    open("photo.jpg", "wb").write(got)
    print(f"saved photo.jpg: {len(got):,} bytes")


if __name__ == "__main__":
    if sys.argv[1] == "send":
        send(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        receive(sys.argv[2])
