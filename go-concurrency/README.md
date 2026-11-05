# Golang Concurrency Will Finally Make Sense After This

Video: https://youtu.be/smsmY_GP7sg  
Written version: https://cloudexplainers.com/golang-concurrency-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/channels/main.go`](lab/channels/main.go)
- [`lab/deadlock/main.go`](lab/deadlock/main.go)
- [`lab/go.mod`](lab/go.mod)
- [`lab/gokeyword/main.go`](lab/gokeyword/main.go)
- [`lab/many/main.go`](lab/many/main.go)
- [`lab/mutex/main.go`](lab/mutex/main.go)
- [`lab/race/main.go`](lab/race/main.go)
- [`lab/sequential/main.go`](lab/sequential/main.go)
- [`lab/suppliers/main.go`](lab/suppliers/main.go)
- [`lab/timeout/main.go`](lab/timeout/main.go)
- [`lab/waitgroup/main.go`](lab/waitgroup/main.go)

## Commands, in the order the video runs them

### Three seconds, then nothing

```sh
# ana@laptop:~/shop$
go run ./sequential
diff sequential/main.go gokeyword/main.go
go run ./gokeyword
```

### What a goroutine is

```sh
# ana@laptop:~/shop$
go run ./many
```

### Waiting for goroutines

```sh
# ana@laptop:~/shop$
go run ./waitgroup
go run ./waitgroup
```

### Channels

```sh
# ana@laptop:~/shop$
go run ./channels
```

### Race conditions

```sh
# ana@laptop:~/shop$
go run ./race
go run ./race
go run ./race
go run -race ./race
```

### When goroutines get stuck

```sh
# ana@laptop:~/shop$
cat deadlock/main.go
go run ./deadlock
go run ./timeout
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
