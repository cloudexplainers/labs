# Golang Pointers in 5 Minutes

Video: https://youtu.be/x6B3_1FLjiw  
Written version: https://cloudexplainers.com/golang-pointers-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/addr/main.go`](lab/steps/addr/main.go)
- [`lab/steps/basics/main.go`](lab/steps/basics/main.go)
- [`lab/steps/copy/main.go`](lab/steps/copy/main.go)
- [`lab/steps/fix/main.go`](lab/steps/fix/main.go)
- [`lab/steps/method/main.go`](lab/steps/method/main.go)
- [`lab/steps/newdog/main.go`](lab/steps/newdog/main.go)
- [`lab/steps/nilfix/main.go`](lab/steps/nilfix/main.go)
- [`lab/steps/nilmap/main.go`](lab/steps/nilmap/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Two walks, zero counted

```sh
# trish@laptop:~/walks$
sed -n '10,19p' main.go
go run .
```

### Go hands over a copy

```sh
# trish@laptop:~/walks$
go run .
```

### The fix: pass the address

```sh
# trish@laptop:~/walks$
go run .
```

### & and * on their own

```sh
# trish@laptop:~/walks$
sed -n '6,12p' main.go
go run .
```

### Methods take the address for you

```sh
# trish@laptop:~/walks$
sed -n '10,18p' main.go
go run .
```

### When a pointer is nil

```sh
# trish@laptop:~/walks$
sed -n '15,17p' main.go
go run .
sed -n '16,21p' main.go
go run .
```

### Returning a pointer

```sh
# trish@laptop:~/walks$
sed -n '10,19p' main.go
go build -gcflags=-m . 2>&1 | grep moved
go run .
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
