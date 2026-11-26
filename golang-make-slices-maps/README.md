# Golang make() for Slices and Maps in 5 Minutes

Video: https://youtu.be/sDCikn_06uI  
Written version: https://cloudexplainers.com/golang-make-for-slices-and-maps-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/bench/main.go`](lab/steps/bench/main.go)
- [`lab/steps/bench/main_test.go`](lab/steps/bench/main_test.go)
- [`lab/steps/growth/main.go`](lab/steps/growth/main.go)
- [`lab/steps/lenbug/main.go`](lab/steps/lenbug/main.go)
- [`lab/steps/lenfix/main.go`](lab/steps/lenfix/main.go)
- [`lab/steps/makemap/main.go`](lab/steps/makemap/main.go)
- [`lab/steps/nilmap/main.go`](lab/steps/nilmap/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Reading works, writing panics

```sh
# trish@laptop:~/harvest$
sed -n '6,10p' main.go
go run .
```

### make for maps

```sh
# trish@laptop:~/harvest$
sed -n '6,12p' main.go
go run .
```

### make for slices: length

```sh
# trish@laptop:~/harvest$
sed -n '8,12p' main.go
go run .
sed -n '8,8p' main.go
go run .
```

### Capacity: room to grow

```sh
# trish@laptop:~/harvest$
sed -n '6,15p' main.go
go run .
sed -n '10,16p' main.go
go test -bench . -benchmem -cpu 1
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
