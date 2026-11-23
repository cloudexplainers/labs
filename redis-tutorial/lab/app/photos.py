import redis

r = redis.Redis(decode_responses=True)

saved = 0
try:
    for i in range(1, 10_001):
        r.set(f"photo:{i}", "x" * 1000)  # a 1 KB thumbnail
        saved += 1
except redis.exceptions.OutOfMemoryError as err:
    print(f"stopped after {saved} photos: {err}")
else:
    print(f"saved all {saved} photos")
print("keys in Redis:", r.dbsize())
