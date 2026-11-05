#!/usr/bin/env python3
"""A pretend video call: one 160-byte audio frame every 20 ms (50 a second), like a real call app.

  python3 call.py send tcp|udp HOST     (on the laptop: 10 seconds of "audio")
  python3 call.py listen tcp|udp        (on the server: counts frames and how late they are)

Each frame carries its number and the moment it was sent. The lab's machines are containers on one
computer and share one clock, so delay = arrival time - send time, measured exactly.
A call app plays each frame about 150 ms after it was spoken (ITU-T G.114); a frame later than that is useless.
"""
import json, socket, statistics, struct, sys, time

PORT, SIZE, EVERY, FRAMES, LATE = 5004, 160, 0.020, 500, 0.150
HDR = struct.Struct("!IId")          # frame number, frames in the call, send time


def send(proto, host):
    if proto == "tcp":
        s = socket.create_connection((host, PORT))
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)   # send each frame at once, like a call app would
        out = s.sendall
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = (socket.gethostbyname(host), PORT)
        out = lambda b: s.sendto(b, addr)
    start = time.time()
    for i in range(FRAMES):
        wait = start + i * EVERY - time.time()
        if wait > 0:
            time.sleep(wait)
        out(HDR.pack(i, FRAMES, time.time()).ljust(SIZE, b"\0"))
    if proto == "tcp":
        s.shutdown(socket.SHUT_WR)
        s.recv(1)                      # wait until the listener has read everything
    print(f"sent {FRAMES} frames over {proto.upper()}, one every {int(EVERY * 1000)} ms")


def listen_tcp():
    delays = {}
    srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("", PORT)); srv.listen(1)
    conn, _ = srv.accept()
    buf = b""
    while True:
        chunk = conn.recv(65536)
        if not chunk:
            break
        now = time.time()
        buf += chunk
        while len(buf) >= SIZE:
            n, total, sent = HDR.unpack(buf[:HDR.size]); buf = buf[SIZE:]
            delays[n] = now - sent
    conn.sendall(b"k")
    conn.close()
    return delays


def listen_udp():
    delays = {}
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.bind(("", PORT))
    while True:
        try:
            data = s.recv(2048)
        except socket.timeout:
            break
        now = time.time()
        n, total, sent = HDR.unpack(data[:HDR.size])
        delays[n] = now - sent
        s.settimeout(2.0)              # the call is over once nothing arrives for 2 s
    return delays


def report(proto, delays):
    ms = [d * 1000 for d in delays.values()]
    on_time = sum(1 for d in ms if d <= LATE * 1000)
    json.dump({str(k): round(v * 1000, 1) for k, v in sorted(delays.items())}, open(f"/tmp/call-{proto}.json", "w"))
    print(f"{proto.upper()} call: {FRAMES} frames sent")
    print(f"arrived:        {len(ms)}")
    print(f"on time:        {on_time}")
    print(f"too late:       {len(ms) - on_time}")
    print(f"lost:           {FRAMES - len(ms)}")
    print(f"typical delay:  {statistics.median(ms):.0f} ms")
    print(f"worst delay:    {max(ms):.0f} ms")


if __name__ == "__main__":
    mode, proto = sys.argv[1], sys.argv[2]
    if mode == "send":
        send(proto, sys.argv[3])
    else:
        report(proto, listen_tcp() if proto == "tcp" else listen_udp())
