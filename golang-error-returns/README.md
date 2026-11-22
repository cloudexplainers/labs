# Golang Error Return Values in 5 Minutes

Video: https://youtu.be/Kx4cRajsd1k  
Written version: https://cloudexplainers.com/golang-error-return-values-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/both/main.go`](lab/steps/both/main.go)
- [`lab/steps/check/main.go`](lab/steps/check/main.go)
- [`lab/steps/ignore/main.go`](lab/steps/ignore/main.go)
- [`lab/steps/own/main.go`](lab/steps/own/main.go)
- [`lab/steps/unused/main.go`](lab/steps/unused/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Three drinks, two prices

```sh
# dave@laptop:~/cart$
sed -n '10,19p' main.go
go run .
```

### Two values come back

```sh
# dave@laptop:~/cart$
sed -n '10,15p' main.go
go run .
```

### What an error is

```sh
# dave@laptop:~/cart$
go doc builtin.error
go run .
```

### Read the error

```sh
# dave@laptop:~/cart$
go run .
```

### Return your own errors

```sh
# dave@laptop:~/cart$
sed -n '10,21p' main.go
go run .
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
