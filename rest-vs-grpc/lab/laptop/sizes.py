# The same Sencha answer, as the bytes each door sends: REST's JSON text, gRPC's protobuf message.
import grpc
import httpx
import stock_pb2
import stock_pb2_grpc

as_json = httpx.get("http://stock:8000/teas/sencha").content
stub = stock_pb2_grpc.StockStub(grpc.insecure_channel("stock:50051"))
as_proto = stub.GetTea(stock_pb2.TeaRequest(name="sencha")).SerializeToString()
print(f"JSON:     {len(as_json)} bytes  {as_json.decode()}")
print(f"protobuf: {len(as_proto)} bytes  {as_proto.hex(' ')}")
