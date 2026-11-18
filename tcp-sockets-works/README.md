# How TCP Sockets Work

Video: https://youtu.be/u1SjuVKn2gY  
Written version: https://cloudexplainers.com/how-tcp-sockets-work/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/kitchen.py`](lab/kitchen.py)
- [`lab/kitchen_lines.py`](lab/kitchen_lines.py)
- [`lab/kitchen_reuse.py`](lab/kitchen_reuse.py)
- [`lab/not_yet.py`](lab/not_yet.py)
- [`lab/tablet.py`](lab/tablet.py)
- [`lab/tablet_lines.py`](lab/tablet_lines.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Two orders, one ticket

```sh
# ana@kitchen:~$
python3 kitchen.py
# ana@tablet1:~$
python3 tablet.py "2 margherita" "1 pepperoni"
# ana@kitchen:~$
python3 kitchen.py
```

### Four calls to open the kitchen

```sh
# ana@kitchen:~$
python3 not_yet.py
ss -tan 'sport = :9000'
# ana@tablet1:~$
python3 tablet.py "4 garlic knots"
# ana@kitchen:~$
ss -tan 'sport = :9000'
python3 not_yet.py
```

### The handshake on the wire

```sh
# ana@tablet1:~$
python3 tablet.py "1 hawaiian"
# ana@kitchen:~$
sudo timeout 6 tcpdump -n -t -l -i eth0 tcp port 9000 2>/dev/null | cut -d, -f1
sudo timeout 12 tcpdump -n -t -l -i eth0 tcp port 9000 2>/dev/null | cut -d, -f1
```

### One port, many tablets

```sh
# ana@kitchen:~$
python3 kitchen.py
ss -tan 'sport = :9000'
# ana@tablet1:~$
python3 tablet.py "1 lasagna"
```

### Where the line between orders went

```sh
# ana@tablet1:~$
python3 tablet.py "2 margherita" "1 pepperoni"
# ana@kitchen:~$
python3 kitchen.py
```

### Hanging up, and the minute after

```sh
# ana@kitchen:~$
python3 kitchen.py
# ana@tablet1:~$
python3 tablet.py "2 margherita" "1 pepperoni"
# ana@kitchen:~$
python3 kitchen.py
ss -tano 'sport = :9000'
grep -n SO_REUSEADDR kitchen.py
python3 kitchen.py
ss -tan 'sport = :9000'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
