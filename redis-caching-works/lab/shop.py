"""Ana's tea shop: the pages that read from PostgreSQL, with Redis as a cache in front (cache-aside)."""
import json
import sys
import threading
import time

import psycopg
import redis

r = redis.Redis(host="cache", decode_responses=True)
DB = "host=db dbname=shop user=shop password=shop"
TTL = 300  # seconds a cached answer is kept

BEST_SQL = """
SELECT p.name, sum(o.qty) AS sold
FROM orders o JOIN products p ON p.id = o.product_id
GROUP BY p.name ORDER BY sold DESC LIMIT 5
"""


def best_sellers_from_db(db):
    rows = db.execute(BEST_SQL).fetchall()
    return [{"name": n, "sold": int(s)} for n, s in rows]


def best_sellers(db, use_cache=True):
    """Cache-aside: ask Redis first; on a miss, ask PostgreSQL and keep the answer for TTL seconds."""
    if use_cache:
        cached = r.get("shop:bestsellers")
        if cached is not None:
            return json.loads(cached), "Redis (cache hit)"
    rows = best_sellers_from_db(db)
    if use_cache:
        r.set("shop:bestsellers", json.dumps(rows), ex=TTL)
        return rows, "PostgreSQL (cache miss)"
    return rows, "PostgreSQL (no cache)"


def product(db, pid):
    key = f"shop:product:{pid}"
    cached = r.get(key)
    if cached is not None:
        return json.loads(cached), "Redis (cache hit)"
    name, cents = db.execute("SELECT name, price_cents FROM products WHERE id = %s", (pid,)).fetchone()
    page = {"name": name, "price": cents / 100}
    r.set(key, json.dumps(page), ex=TTL)
    return page, "PostgreSQL (cache miss)"


def cmd_bestsellers(args):
    with psycopg.connect(DB) as db:
        t = time.perf_counter()
        rows, source = best_sellers(db, use_cache="--no-cache" not in args)
        ms = (time.perf_counter() - t) * 1000
    print(f"from {source}: {ms:.1f} ms")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row['name']:<16} {row['sold']:>9,} sold")


def cmd_price(args):
    with psycopg.connect(DB) as db:
        page, source = product(db, int(args[0]))
    print(f"{page['name']}: ${page['price']:.2f}   (from {source})")


def cmd_set_price(args):
    """Ana's admin page: change a price in the database. --clear-cache also deletes the cached copy."""
    pid, price = int(args[0]), float(args[1])
    with psycopg.connect(DB) as db:
        db.execute("UPDATE products SET price_cents = %s WHERE id = %s", (round(price * 100), pid))
    print(f"database: product {pid} now ${price:.2f}")
    if "--clear-cache" in args:
        print(f"redis: deleted {r.delete(f'shop:product:{pid}')} key")


def cmd_fill(args):
    """Cache a product page for every tea in a big catalogue, 1 KB each."""
    n = int(args[0])
    body = "x" * 1000
    try:
        for i in range(1, n + 1):
            r.set(f"shop:page:{i}", body, ex=3600)
        print(f"cached {n:,} pages")
    except redis.exceptions.ResponseError as e:
        print(f"page {i:,} failed: {e}")


def cmd_rush(args):
    """N visitors open the best sellers page at the same moment, right after the cached copy expired."""
    n, lock = int(args[0]), "--lock" in args
    r.delete("shop:bestsellers")
    sources, times = [], []
    start = threading.Barrier(n)

    def visitor():
        with psycopg.connect(DB) as db:
            start.wait()
            t = time.perf_counter()
            if not lock:
                _, source = best_sellers(db)
            else:
                source = None
                while source is None:
                    cached = r.get("shop:bestsellers")
                    if cached is not None:
                        source = "Redis"
                    elif r.set("lock:bestsellers", "1", nx=True, ex=10):  # only one visitor rebuilds it
                        r.set("shop:bestsellers", json.dumps(best_sellers_from_db(db)), ex=TTL)
                        r.delete("lock:bestsellers")
                        source = "PostgreSQL"
                    else:
                        time.sleep(0.02)  # someone else is rebuilding: wait for Redis
            sources.append(source)
            times.append(time.perf_counter() - t)

    threads = [threading.Thread(target=visitor) for _ in range(n)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    db_count = sum(1 for s in sources if s.startswith("PostgreSQL"))
    print(f"{n} visitors at once{' (with a lock)' if lock else ''}")
    print(f"asked PostgreSQL: {db_count}")
    print(f"served by Redis:  {n - db_count}")
    print(f"slowest visitor:  {max(times) * 1000:,.0f} ms")


if __name__ == "__main__":
    {"bestsellers": cmd_bestsellers, "price": cmd_price, "set-price": cmd_set_price, "fill": cmd_fill,
     "rush": cmd_rush}[sys.argv[1]](sys.argv[2:])
