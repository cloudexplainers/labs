# Linux Processes vs Threads: When Each One Wins

Video: https://youtu.be/86Wzw9MnxFo  
Written version: https://cloudexplainers.com/linux-processes-vs-threads-when-each-one-wins/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/burn.c`](lab/burn.c)
- [`lab/common.h`](lab/common.h)
- [`lab/counter.c`](lab/counter.c)
- [`lab/crash.c`](lab/crash.c)
- [`lab/spawn.c`](lab/spawn.c)

## Commands, in the order the video runs them

### Processes vs threads

```sh
# ana@ubuntu:~$
ps -u postgres -o pid,nlwp,args
ps -C mariadbd -o pid,nlwp,comm
```

### What a process is

```sh
# ana@ubuntu:~$
ls -l /usr/sbin/nginx
ps -C nginx -o pid,user,nlwp,args
```

### What a thread is

```sh
# ana@ubuntu:~$
ps -T -p $(pidof mariadbd) | head -5
ls /proc/$(pidof mariadbd)/task | wc -l
```

### Round 1: Sharing memory

```sh
# ana@ubuntu:~$
counter --processes 4
counter --threads 4
counter --threads 4
counter --threads 4 --lock
```

### Round 2: Crashes

```sh
# ana@ubuntu:~$
crash --threads 4
crash --processes 4
sudo kill -9 40
ps -C nginx -o pid,user,nlwp,args
curl -sI localhost | head -1
```

### Round 3: Starting one

```sh
# ana@ubuntu:~$
spawn --threads 10000
spawn --processes 10000
```

### Round 4: CPU cores

```sh
# ana@ubuntu:~$
nproc
burn --threads 4 & sleep 3; ps -C burn -o pid,nlwp,pcpu,comm; wait
burn --processes 4 & sleep 3; ps -C burn -o pid,nlwp,pcpu,comm; wait
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
