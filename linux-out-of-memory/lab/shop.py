#!/usr/bin/env python3
"""Ana's shop app: a tiny stand-in web shop for P028 "Why Your Linux Server Runs Out of Memory".

A master process starts N worker processes (like gunicorn). Each worker loads the product catalog into
memory (CATALOG_MB of real, touched memory) and answers HTTP on port 8080:
  /            "ok"
  /product     a product page; each one is also kept in a "recently viewed" cache (PAGE_MB each) that has no
               limit and is never cleared: the bug
  /report      the yearly sales report: 1.0 builds all REPORT_MB in memory at once; 1.1 a piece at a time
Settings come from the environment (WORKERS, CATALOG_MB, PAGE_MB, REPORT_MB), as from a systemd unit.
Process names: "shop" (the master) and "shop-worker".
"""
import collections
import http.server
import os
import signal
import socket
import sys
import time

VERSION = "1.0"   # demo.sh makes the fixed 1.1 from this file by changing only this line
FIXED = VERSION != "1.0"
RECENT_LIMIT = 20  # 1.1: keep only the last 20 pages
CHUNK_MB = 20      # 1.1: build the report 20 MB at a time
WORKERS = int(os.environ.get("WORKERS", "2"))
CATALOG_MB = int(os.environ.get("CATALOG_MB", "100"))
PAGE_MB = int(os.environ.get("PAGE_MB", "1"))
REPORT_MB = int(os.environ.get("REPORT_MB", "400"))
MB = 1024 * 1024


def touched(mb: int) -> bytearray:
    """mb of memory the kernel really has to give us (every page written)."""
    return bytearray(b"\x01") * (mb * MB)


class Shop(http.server.BaseHTTPRequestHandler):
    catalog = None
    recently_viewed = collections.OrderedDict()   # 1.0's bug: grows with every request, never cleared
    served = 0

    def log_message(self, *a):
        pass

    def answer(self, text: str):
        body = (text + "\n").encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        Shop.served += 1
        if self.path == "/product":
            Shop.recently_viewed[Shop.served] = touched(PAGE_MB)
            if FIXED and len(Shop.recently_viewed) > RECENT_LIMIT:
                Shop.recently_viewed.popitem(last=False)
            self.answer("product page")
        elif self.path == "/report":
            if FIXED:   # one piece at a time: each piece is summed, then dropped
                done = 0
                while done < REPORT_MB:
                    piece = touched(min(CHUNK_MB, REPORT_MB - done))
                    done += len(piece) // MB
                    del piece
                self.answer(f"report ready ({done} MB of sales, {CHUNK_MB} MB at a time)")
            else:       # 1.0: the whole year in memory at once
                rows = touched(REPORT_MB)
                self.answer(f"report ready ({len(rows) // MB} MB of sales)")
                del rows
        else:
            self.answer("ok")


def name(comm: str):
    with open("/proc/self/comm", "w") as f:
        f.write(comm)


def worker():
    name("shop-worker")
    Shop.catalog = touched(CATALOG_MB)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind(("0.0.0.0", 8080))
    s.listen(64)
    srv = http.server.HTTPServer(("0.0.0.0", 8080), Shop, bind_and_activate=False)
    srv.socket = s
    srv.serve_forever()


def start_worker() -> int:
    pid = os.fork()
    if pid == 0:
        try:
            worker()
        finally:
            os._exit(0)
    return pid


def main():
    name("shop")
    kids = [start_worker() for _ in range(WORKERS)]
    print(f"shop {VERSION}: {WORKERS} workers, catalog {CATALOG_MB} MB each", flush=True)

    def stop(*_):
        for k in kids:
            try:
                os.kill(k, signal.SIGTERM)
            except ProcessLookupError:
                pass
        sys.exit(0)
    signal.signal(signal.SIGTERM, stop)
    while True:                  # like gunicorn: a worker that dies is replaced
        pid, status = os.wait()
        how = f"signal {os.WTERMSIG(status)}" if os.WIFSIGNALED(status) else f"exit {os.WEXITSTATUS(status)}"
        print(f"shop: worker {pid} died ({how}), starting a new one", flush=True)
        kids.remove(pid)
        time.sleep(1)
        kids.append(start_worker())


if __name__ == "__main__":
    main()
