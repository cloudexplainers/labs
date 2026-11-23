import redis

r = redis.Redis(decode_responses=True)

print("waiting for jobs...", flush=True)
while True:
    _, job = r.brpop("jobs")  # waits until a job arrives
    car = r.hget(f"job:{job}", "car")
    print(f"job {job}: {car}", flush=True)
