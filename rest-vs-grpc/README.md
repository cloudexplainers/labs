# REST vs gRPC: Which One Should You Use?

Video: https://youtu.be/6wxOAufNZzM  
Written version: https://cloudexplainers.com/rest-vs-grpc-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/laptop/bench.py`](lab/laptop/bench.py)
- [`lab/laptop/check_grpc.py`](lab/laptop/check_grpc.py)
- [`lab/laptop/check_rest.py`](lab/laptop/check_rest.py)
- [`lab/laptop/sizes.py`](lab/laptop/sizes.py)
- [`lab/laptop/stock.proto`](lab/laptop/stock.proto)
- [`lab/stock/shop_server.py`](lab/stock/shop_server.py)
- [`lab/stock/stock.proto`](lab/stock/stock.proto)
- [`lab/stock/v2/stock.proto`](lab/stock/v2/stock.proto)
- [`lab/stock/v3/stock.proto`](lab/stock/v3/stock.proto)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Two ways to ask one question

```sh
# (.venv) ana@laptop:~/order-service$
curl -s stock:8000/teas/sencha
curl -sS stock:50051/teas/sencha
```

### How REST asks

```sh
# (.venv) ana@laptop:~/order-service$
cat check_rest.py
python3 check_rest.py
```

### How gRPC asks

```sh
# (.venv) ana@laptop:~/order-service$
cat stock.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. stock.proto
ls
cat check_grpc.py
python3 check_grpc.py
grpcurl -plaintext -proto stock.proto -d '{"name": "sencha"}' stock:50051 Stock/GetTea
grpcurl -v -plaintext -proto stock.proto -d '{"name": "sencha"}' stock:50051 Stock/GetTea | grep content-type
```

### Smaller and faster, by how much?

```sh
# (.venv) ana@laptop:~/order-service$
python3 sizes.py
python3 bench.py 10000
```

### When the answer keeps changing

```sh
# (.venv) ana@laptop:~/order-service$
grpcurl -plaintext -proto stock.proto -d '{"name": "sencha"}' stock:50051 Stock/WatchStock
curl -s stock:8000/orders -H "Content-Type: application/json" -d '{"tea": "sencha", "qty": 2}'
curl -s stock:8000/orders -H "Content-Type: application/json" -d '{"tea": "sencha", "qty": 2}'
grpcurl -plaintext -proto stock.proto -d '{"name": "sencha"}' stock:50051 Stock/WatchStock
```

### When the API changes

```sh
# (.venv) ana@stock:~/stock-service$
diff stock.proto v2/stock.proto
python3 shop_server.py --v2
# (.venv) ana@laptop:~/order-service$
curl -s stock:8000/teas/sencha
python3 check_rest.py
python3 check_grpc.py
# (.venv) ana@stock:~/stock-service$
diff stock.proto v3/stock.proto
# (.venv) ana@laptop:~/order-service$
python3 check_grpc.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
