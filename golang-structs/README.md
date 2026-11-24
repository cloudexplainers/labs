# Golang Structs in 5 Minutes

Video: https://youtu.be/LEbAMoq3n0I  
Written version: https://cloudexplainers.com/golang-structs-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/added/main.go`](lab/steps/added/main.go)
- [`lab/steps/badtag/main.go`](lab/steps/badtag/main.go)
- [`lab/steps/copy/main.go`](lab/steps/copy/main.go)
- [`lab/steps/exported/main.go`](lab/steps/exported/main.go)
- [`lab/steps/json/main.go`](lab/steps/json/main.go)
- [`lab/steps/keyed/main.go`](lab/steps/keyed/main.go)
- [`lab/steps/pointer/main.go`](lab/steps/pointer/main.go)
- [`lab/steps/positional/main.go`](lab/steps/positional/main.go)
- [`lab/steps/zero/main.go`](lab/steps/zero/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One new field, three errors

```sh
# sue@laptop:~/arcade$
go run .
```

### What a struct is

```sh
# sue@laptop:~/arcade$
sed -n '13,15p' main.go
go run .
```

### Write the field names

```sh
# sue@laptop:~/arcade$
go run .
```

### A copy, not the original

```sh
# sue@laptop:~/arcade$
sed -n '17,20p' main.go
go run .
sed -n '17,20p' main.go
go run .
```

### Capital letters and tags

```sh
# sue@laptop:~/arcade$
sed -n '8,13p' main.go
go run .
sed -n '12,12p' main.go
go run .
sed -n '9,9p' main.go
go run .
go vet .
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
