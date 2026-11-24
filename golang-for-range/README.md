# Golang for range Loops in 5 Minutes

Video: https://youtu.be/qJajUCGAYp8  
Written version: https://cloudexplainers.com/golang-for-range-loops-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/copy/main.go`](lab/steps/copy/main.go)
- [`lab/steps/count/main.go`](lab/steps/count/main.go)
- [`lab/steps/fixed/main.go`](lab/steps/fixed/main.go)
- [`lab/steps/index/main.go`](lab/steps/index/main.go)
- [`lab/steps/maporder/main.go`](lab/steps/maporder/main.go)
- [`lab/steps/sorted/main.go`](lab/steps/sorted/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### The loop that changed nothing

```sh
# joe@laptop:~/catchlog$
sed -n '19,23p' main.go
go run .
```

### What range hands you

```sh
# joe@laptop:~/catchlog$
sed -n '19,21p' main.go
go run .
```

### Change the log, not a copy

```sh
# joe@laptop:~/catchlog$
go run .
```

### Range over a number

```sh
# joe@laptop:~/catchlog$
sed -n '6,8p' main.go
go run .
```

### Ranging over a map

```sh
# joe@laptop:~/catchlog$
sed -n '23,30p' main.go
for n in 1 2 3; do go run .; done
sed -n '31,33p' main.go
for n in 1 2 3; do go run .; done
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
