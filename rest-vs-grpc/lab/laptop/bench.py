# Ask for Sencha N times through each door, one call after another, reusing one connection each, and time it.
import sys
import time

import grpc
import httpx
import stock_pb2
import stock_pb2_grpc

n = int(sys.argv[1])
rest = httpx.Client()
stub = stock_pb2_grpc.StockStub(grpc.insecure_channel("stock:50051"))
rest.get("http://stock:8000/teas/sencha")
stub.GetTea(stock_pb2.TeaRequest(name="sencha"))

t = time.perf_counter()
for _ in range(n):
    rest.get("http://stock:8000/teas/sencha").json()
r = time.perf_counter() - t
t = time.perf_counter()
for _ in range(n):
    stub.GetTea(stock_pb2.TeaRequest(name="sencha"))
g = time.perf_counter() - t
print(f"REST: {n:,} calls in {r:.2f} s  ({r / n * 1000:.2f} ms each)")
print(f"gRPC: {n:,} calls in {g:.2f} s  ({g / n * 1000:.2f} ms each)")
