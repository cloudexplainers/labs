import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print(r.get("cars:today"))
print(r.hgetall("job:1001"))
