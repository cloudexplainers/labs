# Linux Makefiles Will Finally Make Sense After This

Video: https://youtu.be/GVKhuIO-ULk  
Written version: https://cloudexplainers.com/linux-makefiles-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/mk/Makefile.spaces`](lab/mk/Makefile.spaces)
- [`lab/mk/Makefile.v1`](lab/mk/Makefile.v1)
- [`lab/mk/Makefile.v2`](lab/mk/Makefile.v2)
- [`lab/mk/Makefile.v3`](lab/mk/Makefile.v3)
- [`lab/mk/Makefile.v4`](lab/mk/Makefile.v4)
- [`lab/mk/Makefile.v4b`](lab/mk/Makefile.v4b)
- [`lab/mk/Makefile.v5`](lab/mk/Makefile.v5)
- [`lab/src/fares.c`](lab/src/fares.c)
- [`lab/src/fares.h`](lab/src/fares.h)
- [`lab/src/main.c`](lab/src/main.c)
- [`lab/src/times.c`](lab/src/times.c)
- [`lab/src/times.c.v2`](lab/src/times.c.v2)
- [`lab/src/times.h`](lab/src/times.h)
- [`lab/src/times.h.late`](lab/src/times.h.late)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Missing separator

```sh
# ana@office:~$
cat Makefile
make
```

### One idea: the rule

```sh
# ana@office:~$
cat -T Makefile
```

### The first build

```sh
# ana@office:~$
make
./ferry
make
```

### How does make know?

```sh
# ana@office:~$
ls -l --time-style=+%T times.c times.o
make
touch fares.c
make
```

### The change make can't see

```sh
# ana@office:~$
cat times.h
grep LAST times.h
make
./ferry
grep '\.h' Makefile
make -n
make
./ferry
```

### Targets that aren't files

```sh
# ana@office:~$
tail -n 2 Makefile
make clean
ls
touch clean
make clean
tail -n 3 Makefile
make clean
tail -n 2 Makefile
make run
touch times.c
make run
```

### Three messages you'll meet

```sh
# ana@office:/tmp$
make
# ana@office:~$
make claen
mv fares.c fares.c.bak
make
```

### Reading the dollar signs

```sh
# ana@office:~$
head -n 9 Makefile
```

### Does it matter on a real project?

```sh
# ana@office:~/lua$
ls src/*.c | wc -l
time make > build.log
grep -c gcc build.log
touch src/lvm.c
time make > build.log
grep -c gcc build.log
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
