# Golang REST API with Gin: Full Tutorial for Beginners

Video: https://youtu.be/IbJs0sDK8Sk  
Written version: https://cloudexplainers.com/golang-rest-api-with-gin-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/s1/main.go`](lab/steps/s1/main.go)
- [`lab/steps/s10/handlers.go`](lab/steps/s10/handlers.go)
- [`lab/steps/s10/main.go`](lab/steps/s10/main.go)
- [`lab/steps/s10/main_test.go`](lab/steps/s10/main_test.go)
- [`lab/steps/s10/middleware.go`](lab/steps/s10/middleware.go)
- [`lab/steps/s10/store.go`](lab/steps/s10/store.go)
- [`lab/steps/s10bug/handlers.go`](lab/steps/s10bug/handlers.go)
- [`lab/steps/s2/main.go`](lab/steps/s2/main.go)
- [`lab/steps/s3/main.go`](lab/steps/s3/main.go)
- [`lab/steps/s4/handlers.go`](lab/steps/s4/handlers.go)
- [`lab/steps/s4/main.go`](lab/steps/s4/main.go)
- [`lab/steps/s4/store.go`](lab/steps/s4/store.go)
- [`lab/steps/s5/handlers.go`](lab/steps/s5/handlers.go)
- [`lab/steps/s5/main.go`](lab/steps/s5/main.go)
- [`lab/steps/s5/store.go`](lab/steps/s5/store.go)
- [`lab/steps/s6/handlers.go`](lab/steps/s6/handlers.go)
- [`lab/steps/s6/main.go`](lab/steps/s6/main.go)
- [`lab/steps/s6/store.go`](lab/steps/s6/store.go)
- [`lab/steps/s7/handlers.go`](lab/steps/s7/handlers.go)
- [`lab/steps/s7/main.go`](lab/steps/s7/main.go)
- [`lab/steps/s7/store.go`](lab/steps/s7/store.go)
- [`lab/steps/s8/handlers.go`](lab/steps/s8/handlers.go)
- [`lab/steps/s8/main.go`](lab/steps/s8/main.go)
- [`lab/steps/s8/store.go`](lab/steps/s8/store.go)
- [`lab/steps/s9/handlers.go`](lab/steps/s9/handlers.go)
- [`lab/steps/s9/main.go`](lab/steps/s9/main.go)
- [`lab/steps/s9/middleware.go`](lab/steps/s9/middleware.go)
- [`lab/steps/s9/store.go`](lab/steps/s9/store.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Every plant came back empty

```sh
# ana@laptop:~/nursery$
curl localhost:8080/plants
sed -n '9,20p' main.go
```

### Go, a module and Gin

```sh
# ana@laptop:~$
go version
mkdir nursery && cd nursery
# ana@laptop:~/nursery$
go mod init nursery
cat main.go
go mod tidy
head -n 5 go.mod
ls
```

### Your first route

```sh
# ana@laptop:~/nursery$
go run .
curl localhost:8080/ping
curl -i localhost:8080/ping
curl -i localhost:8080/plants
```

### From a struct to JSON

```sh
# ana@laptop:~/nursery$
go run .
sed -n '9,14p' main.go
curl localhost:8080/plants
curl -s localhost:8080/plants | jq -c '.[]'
```

### One plant by its id

```sh
# ana@laptop:~/nursery$
ls
cat main.go
sed -n '10,16p' store.go
sed -n '/^func getPlant/,/^}/p' handlers.go
curl localhost:8080/plants/2
curl localhost:8080/plants/abc
sed -n '/^func getPlant/,/^}/p' handlers.go
curl -i localhost:8080/plants/abc
curl -i localhost:8080/plants/9
```

### Filtering with a query

```sh
# ana@laptop:~/nursery$
sed -n '/^func listPlants/,/^}/p' handlers.go
curl "localhost:8080/plants?light=shade"
curl -s "localhost:8080/plants?light=sun" | jq -c '.[]'
```

### Adding plants with POST

```sh
# ana@laptop:~/nursery$
sed -n '/^type NewPlant/,/^}/p' handlers.go
sed -n '/^func createPlant/,/^}/p' handlers.go
curl -i -X POST localhost:8080/plants -d '{"name":"Mint","light":"sun","stock":5}'
curl -X POST localhost:8080/plants -d '{"light":"sun","stock":5}'
curl -X POST localhost:8080/plants -d '{"name":"Mint","light":"moon","stock":5}'
curl -X POST localhost:8080/plants -d '{"name":"Mint","light":"sun","stock":"five"}'
curl -s localhost:8080/plants | jq length
curl -s localhost:8080/plants | jq length
```

### Changing and deleting

```sh
# ana@laptop:~/nursery$
grep -n 'r\.' main.go
sed -n '/^func deletePlant/,/^}/p' handlers.go
curl -X PUT localhost:8080/plants/3 -d '{"name":"Olive tree","light":"sun","stock":7}'
curl -i -X DELETE localhost:8080/plants/1
curl -i -X DELETE localhost:8080/plants/1
curl -s localhost:8080/plants | jq -c '.[]'
```

### Many requests at once

```sh
# ana@laptop:~/nursery$
seq 300 | xargs -P 30 -I{} curl -s -o /dev/null -X POST localhost:8080/plants -d '{"name":"Mint","light":"sun","stock":5}'; echo done
curl localhost:8080/plants
tail -n 2 store.go
sed -n '/^func createPlant/,/^}/p' handlers.go
seq 300 | xargs -P 30 -I{} curl -s -o /dev/null -X POST localhost:8080/plants -d '{"name":"Mint","light":"sun","stock":5}'; echo done
curl -s localhost:8080/plants | jq length
```

### Middleware and a key

```sh
# ana@laptop:~/nursery$
cat middleware.go
sed -n '/^func main/,/^}/p' main.go
curl -i -X POST localhost:8080/plants -d '{"name":"Mint","light":"sun","stock":5}'
curl -i -X POST localhost:8080/plants -d '{"name":"Mint","light":"sun","stock":5}'
curl -i -X POST localhost:8080/plants -H 'X-API-Key: green-thumb-42' -d '{"name":"Mint","light":"sun","stock":5}'
sed -n '/^func main/,/^}/p' main.go
```

### Tests

```sh
# ana@laptop:~/nursery$
sed -n '17,25p' main_test.go
go test -v
go test
go test
```

### One file to ship

```sh
# ana@laptop:~/nursery$
go build -o nursery-api
ls -lh nursery-api
GIN_MODE=release NURSERY_KEY=green-thumb-42 ./nursery-api
curl localhost:8080/plants/2
GOOS=windows GOARCH=amd64 go build -o nursery-api.exe
file nursery-api.exe
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
