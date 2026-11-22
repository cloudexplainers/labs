# How to Fix Golang 'go.mod File Not Found' Errors

Video: https://youtu.be/NQ7Xs6oYEQ4  
Written version: https://cloudexplainers.com/how-to-fix-golang-go-mod-file-not-found-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/alerts/main.go`](lab/steps/alerts/main.go)
- [`lab/steps/board/main.go`](lab/steps/board/main.go)
- [`lab/steps/color/main.go`](lab/steps/color/main.go)
- [`lab/steps/docker_bad/Dockerfile`](lab/steps/docker_bad/Dockerfile)
- [`lab/steps/docker_good/Dockerfile`](lab/steps/docker_good/Dockerfile)
- [`lab/steps/rail_board/main.go`](lab/steps/rail_board/main.go)
- [`lab/steps/tools/main.go`](lab/steps/tools/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### The usual fix: go mod init

```sh
# sue@laptop:~/departures$
go run main.go
go run .
go mod init
go mod init departures
go run .
```

### What go.mod is for

```sh
# sue@laptop:~/departures$
cat go.mod
go env GOMOD
sed -n '3,7p' main.go
go run .
go mod tidy
cat go.mod
go run .
cd /tmp/loose
# sue@laptop:/tmp/loose$
go run main.go
```

### Run from the wrong folder

```sh
# sue@laptop:~/departures/tools$
go run .
go env GOMOD
cd ~
# sue@laptop:~$
go run ./departures
go env GOMOD
```

### Two projects in one folder

```sh
# rich@laptop:~/rail$
ls */
go run ./alerts
go work init ./board ./alerts
cat go.work
go run ./alerts
```

### Inside a Docker build

```sh
# sue@laptop:~/departures$
cat Dockerfile
docker build -t board . 2>&1 | tail -12
docker build -t board . 2>&1 | tail -2
docker run --rm board
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
