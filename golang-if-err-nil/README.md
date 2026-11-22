# Golang if err != nil Checks in 5 Minutes

Video: https://youtu.be/91PZUTWD0Pg  
Written version: https://cloudexplainers.com/golang-if-err-nil-checks-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/inside/main.go`](lab/steps/inside/main.go)
- [`lab/steps/is/main.go`](lab/steps/is/main.go)
- [`lab/steps/isv/main.go`](lab/steps/isv/main.go)
- [`lab/steps/noreturn/main.go`](lab/steps/noreturn/main.go)
- [`lab/steps/ret/main.go`](lab/steps/ret/main.go)
- [`lab/steps/wrap/main.go`](lab/steps/wrap/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Printed, then crashed

```sh
# joe@laptop:~/flights$
sed -n '25,31p' main.go
go run .
```

### Return early

```sh
# joe@laptop:~/flights$
go run .
cat schedule.json
go run .
sed -n '13,23p' main.go
```

### Wrap with %w

```sh
# joe@laptop:~/flights$
sed -n '13,23p' main.go
go run .
go run .
```

### Check the kind with errors.Is

```sh
# joe@laptop:~/flights$
sed -n '27,37p' main.go
go run .
grep -n Errorf main.go
go run .
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
