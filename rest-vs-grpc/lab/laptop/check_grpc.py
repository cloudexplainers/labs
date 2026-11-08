# The same question over gRPC: call GetTea like a function, with code generated from stock.proto.
import grpc
import stock_pb2
import stock_pb2_grpc

stub = stock_pb2_grpc.StockStub(grpc.insecure_channel("stock:50051"))
tea = stub.GetTea(stock_pb2.TeaRequest(name="sencha"))
print(f"{tea.name}: {tea.stock} in stock")
