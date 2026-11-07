# Why Golang Uses Goroutines Instead of Threads

Video: https://youtu.be/e_A4fPAZJS4  
Written version: https://cloudexplainers.com/why-golang-uses-goroutines-instead-of-threads/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/blocking/main.go`](lab/blocking/main.go)
- [`lab/c/grow.c`](lab/c/grow.c)
- [`lab/c/switch.c`](lab/c/switch.c)
- [`lab/c/threads.c`](lab/c/threads.c)
- [`lab/go.mod`](lab/go.mod)
- [`lab/goroutines/main.go`](lab/goroutines/main.go)
- [`lab/grow/main.go`](lab/grow/main.go)
- [`lab/switch/main.go`](lab/switch/main.go)

## Commands, in the order the video runs them

### What a thread costs

```sh
# ana@laptop:~/shop$
c/threads 10000
c/threads 100000
cat /proc/sys/kernel/threads-max
```

### What a goroutine is

```sh
# ana@laptop:~/shop$
go run ./goroutines 10000
go run ./goroutines 100000
go run ./goroutines 1000000
```

### Stacks that grow

```sh
# ana@laptop:~/shop$
ulimit -s
c/grow
go run ./grow
```

### Switching for less

```sh
# ana@laptop:~/shop$
c/switch
go run ./switch
```

### When Go needs a thread

```sh
# ana@laptop:~/shop$
go run ./blocking
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
