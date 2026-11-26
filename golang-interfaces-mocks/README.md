# Golang Interfaces and Mocks in 5 Minutes

Video: https://youtu.be/mjI6LP72ULU  
Written version: https://cloudexplainers.com/golang-interfaces-and-mocks-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/cardsvc/main.go`](lab/cardsvc/main.go)
- [`lab/steps/iface/main.go`](lab/steps/iface/main.go)
- [`lab/steps/iface/sell_test.go`](lab/steps/iface/sell_test.go)
- [`lab/steps/missing/main.go`](lab/steps/missing/main.go)
- [`lab/steps/missing/sell_test.go`](lab/steps/missing/sell_test.go)
- [`lab/steps/mock/main.go`](lab/steps/mock/main.go)
- [`lab/steps/mock/sell_test.go`](lab/steps/mock/sell_test.go)
- [`lab/steps/real/main.go`](lab/steps/real/main.go)
- [`lab/steps/real/sell_test.go`](lab/steps/real/sell_test.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One test, two results

```sh
# tom@laptop:~/eggs$
sed -n '28,34p' main.go
```

### An interface is a list of methods

```sh
# tom@laptop:~/eggs$
sed -n '10,13p' main.go
sed -n '41,49p' main.go
go run .
grep -n 'CashBox) Take' main.go
go build .
```

### A fake card reader for tests

```sh
# tom@laptop:~/eggs$
sed -n '9,17p' sell_test.go
sed -n '19,27p' sell_test.go
sed -n '30,39p' sell_test.go
go test -v
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
