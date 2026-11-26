# Golang defer Statements in 5 Minutes

Video: https://youtu.be/S1FbDDUb3Yg  
Written version: https://cloudexplainers.com/golang-defer-statements-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/args/main.go`](lab/steps/args/main.go)
- [`lab/steps/argsfix/main.go`](lab/steps/argsfix/main.go)
- [`lab/steps/early/main.go`](lab/steps/early/main.go)
- [`lab/steps/loopbug/main.go`](lab/steps/loopbug/main.go)
- [`lab/steps/loopfix/main.go`](lab/steps/loopfix/main.go)
- [`lab/steps/order/main.go`](lab/steps/order/main.go)
- [`lab/steps/panic/main.go`](lab/steps/panic/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Two thousand logs, one crash

```sh
# rich@laptop:~/patch$
sed -n '14,21p' main.go
go run .
```

### When a deferred call runs

```sh
# rich@laptop:~/patch$
sed -n '5,12p' main.go
go run .
sed -n '5,8p' main.go
go run .
go run .
```

### The value is saved at once

```sh
# rich@laptop:~/patch$
sed -n '6,9p' main.go
go run .
sed -n '7,9p' main.go
go run .
```

### Why the loop ran out of files

```sh
# rich@laptop:~/patch$
sed -n '26,33p' main.go
go run .
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
