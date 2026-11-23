# Golang Method Receivers in 5 Minutes

Video: https://youtu.be/o3n6m7B-JNo  
Written version: https://cloudexplainers.com/golang-method-receivers-in-5-minutes/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/iface/BROKEN`](lab/steps/iface/BROKEN)
- [`lab/steps/iface/main.go`](lab/steps/iface/main.go)
- [`lab/steps/ifacefix/main.go`](lab/steps/ifacefix/main.go)
- [`lab/steps/mapfix/main.go`](lab/steps/mapfix/main.go)
- [`lab/steps/maps/BROKEN`](lab/steps/maps/BROKEN)
- [`lab/steps/maps/main.go`](lab/steps/maps/main.go)
- [`lab/steps/pointer/main.go`](lab/steps/pointer/main.go)
- [`lab/steps/value/main.go`](lab/steps/value/main.go)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Two wins, and the season says 0

```sh
# jim@laptop:~/league$
sed -n '10,20p' main.go
go run .
```

### The pointer receiver

```sh
# jim@laptop:~/league$
go run .
```

### Interfaces need the address

```sh
# jim@laptop:~/league$
sed -n '18,26p' main.go
go run .
grep -n 'var s' main.go
go run .
```

### Maps need pointers

```sh
# jim@laptop:~/league$
sed -n '14,21p' main.go
go run .
sed -n '15,18p' main.go
go run .
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
