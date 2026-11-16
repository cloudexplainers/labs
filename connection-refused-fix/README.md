# How to Fix Network 'Connection Refused' Errors

Video: https://youtu.be/P7AhcDs0OYQ  
Written version: https://cloudexplainers.com/how-to-fix-network-connection-refused-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/lanes/app.py`](lab/lanes/app.py)
- [`lab/lanes/book.py`](lab/lanes/book.py)
- [`lab/lanes/lanes.service`](lab/lanes/lanes.service)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Refused, but the server is up

```sh
# ana@front-desk:~$
python3 book.py
ping -n -c 2 lanes
```

### Is the app running?

```sh
# ana@lanes:~$
systemctl status lanes
sudo systemctl enable --now lanes
systemctl status lanes
# ana@front-desk:~$
python3 book.py
```

### Listening, but on which address?

```sh
# ana@lanes:~$
sudo ss -ltnp
curl -s localhost:5000/lanes
# ana@front-desk:~$
nc -vz localhost 5000
```

### The fix: listen on every address

```sh
# ana@lanes:~$
sudo systemctl restart lanes
sudo ss -ltnp
# ana@front-desk:~$
python3 book.py
```

### Same error, other words

```sh
# ana@front-desk:~$
curl http://lanes:8000/lanes
curl -v http://lanes:8000/lanes
ssh lanes
```

### Right server, wrong port

```sh
# ana@front-desk:~$
nc -vz lanes 8000
nc -vz lanes 5000
```

### When the firewall says no

```sh
# ana@front-desk:~$
python3 book.py
# ana@lanes:~$
sudo ss -ltnp
sudo ufw status
sudo tcpdump -ni eth0 -ttt -c 2 tcp port 5000
sudo ufw deny 5000/tcp
# ana@front-desk:~$
time nc -vz -w 10 lanes 5000
# ana@lanes:~$
sudo ufw allow 5000/tcp
# ana@front-desk:~$
python3 book.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
