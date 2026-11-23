# Golang context.Context in 5 Minutes

Video: https://youtu.be/omLFM3VDPPg  
Written version: https://cloudexplainers.com/golang-context-context-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/care/main.go`](lab/steps/care/main.go)
- [`lab/steps/carefix/main.go`](lab/steps/carefix/main.go)
- [`lab/steps/ctx/main.go`](lab/steps/ctx/main.go)
- [`lab/steps/noctx/main.go`](lab/steps/noctx/main.go)
- [`lab/steps/timeout/main.go`](lab/steps/timeout/main.go)
- [`lab/steps/vet/main.go`](lab/steps/vet/main.go)
- [`lab/supplier/main.go`](lab/supplier/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### 6 seconds of work for nobody

```sh
# john@laptop:~/garden$
curl --max-time 2 'localhost:8080/stock?plant=fern'
go run .
```

### Pass it down

```sh
# john@laptop:~/garden$
curl --max-time 2 'localhost:8080/stock?plant=fern'
go run .
```

### A deadline of your own

```sh
# john@laptop:~/garden$
sed -n '30,32p' main.go
curl 'localhost:8080/stock?plant=fern'
go run .
```

### Your code has to listen

```sh
# john@laptop:~/garden$
sed -n '43,46p' main.go
curl --max-time 2.5 'localhost:8080/care?plant=fern'
go run .
sed -n '43,53p' main.go
curl --max-time 2.5 'localhost:8080/care?plant=fern'
go run .
```

### The rules

```sh
# john@laptop:~/garden$
sed -n '30p' main.go
go vet .
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
