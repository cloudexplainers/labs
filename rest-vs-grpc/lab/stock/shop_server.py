"""Ana's stock service: the same tea stock behind two doors.

REST (FastAPI on port 8000): GET /teas/<name> answers JSON, POST /orders sells tea.
gRPC (port 50051): Stock.GetTea answers one Tea, Stock.WatchStock streams a Tea every time its stock changes.
--v2 renames the stock field: "in_stock" in the JSON, and field 2 renamed in v2/stock.proto (same number).
--v3 renames it and also gives it a new number, 4 (v3/stock.proto): the mistake the protobuf docs warn about.
"""
import sys
import threading
from concurrent import futures
from pathlib import Path

import grpc
import uvicorn
from fastapi import FastAPI, HTTPException
from grpc_tools import protoc

VER = "v3" if "--v3" in sys.argv else "v2" if "--v2" in sys.argv else ""
HERE = Path(__file__).parent
SRC = HERE / VER
OUT = HERE / f"gen{VER}"
OUT.mkdir(exist_ok=True)
protoc.main(["protoc", f"-I{SRC}", f"--python_out={OUT}", f"--grpc_python_out={OUT}", str(SRC / "stock.proto")])
sys.path.insert(0, str(OUT))
import stock_pb2, stock_pb2_grpc  # noqa: E402

FIELD = "in_stock" if VER else "stock"
TEAS = {"sencha": ["Sencha", 12, 650], "assam": ["Assam", 30, 420], "rooibos": ["Rooibos", 8, 480]}
changed = threading.Condition()


def as_message(key):
    name, left, cents = TEAS[key]
    return stock_pb2.Tea(name=name, cents=cents, **{FIELD: left})


# ------------------------------------------------------------------ REST
api = FastAPI()


@api.get("/teas/{key}")
def get_tea(key: str):
    if key not in TEAS:
        raise HTTPException(404, "no such tea")
    name, left, cents = TEAS[key]
    return {"name": name, FIELD: left, "cents": cents}


@api.post("/orders")
def order(body: dict):
    key, qty = body["tea"], int(body.get("qty", 1))
    with changed:
        TEAS[key][1] -= qty
        changed.notify_all()
    return {"ok": True, "tea": TEAS[key][0], "left": TEAS[key][1]}


# ------------------------------------------------------------------ gRPC
class Stock(stock_pb2_grpc.StockServicer):
    def GetTea(self, request, context):
        if request.name not in TEAS:
            context.abort(grpc.StatusCode.NOT_FOUND, "no such tea")
        return as_message(request.name)

    def WatchStock(self, request, context):
        last = None
        while context.is_active():
            with changed:
                if TEAS[request.name][1] == last:
                    changed.wait(timeout=1)
                    continue
                last = TEAS[request.name][1]
                msg = as_message(request.name)
            yield msg


server = grpc.server(futures.ThreadPoolExecutor(max_workers=16))
stock_pb2_grpc.add_StockServicer_to_server(Stock(), server)
server.add_insecure_port("0.0.0.0:50051")
server.start()
print(f"stock service {VER + ' ' if VER else ''}ready: REST on port 8000, gRPC on port 50051", flush=True)
uvicorn.run(api, host="0.0.0.0", port=8000, log_level="warning")
