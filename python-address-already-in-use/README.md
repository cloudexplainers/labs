# How to Fix Python 'Address Already in Use' Errors

Video: https://youtu.be/WmF1RtSwrSU  
Written version: https://cloudexplainers.com/how-to-fix-python-address-already-in-use-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/files/collector.py`](lab/files/collector.py)
- [`lab/files/dashboard.py`](lab/files/dashboard.py)
- [`lab/files/sensor.py`](lab/files/sensor.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Port 5000 is taken

```sh
# ana@greenhouse:~/greenhouse$
python3 dashboard.py
```

### Find who holds the port

```sh
ss -ltnp 'sport = :5000'
sudo ss -ltnp 'sport = :5000'
# ana@greenhouse:~/greenhouse$
ps -o user,pid,etime,cmd -p 14
sudo kill 14
sudo ss -ltnp 'sport = :5000'
```

### Paused is not stopped

```sh
# ana@greenhouse:~/greenhouse$
python3 dashboard.py
python3 dashboard.py
jobs
curl -m 3 localhost:5000
fg
```

### When it's not yours to stop

```sh
# ana@greenhouse:~/greenhouse$
flask --app dashboard run --port 5001
```

### It fails right after a restart

```sh
# ana@greenhouse:~/greenhouse$
python3 collector.py
python3 collector.py
sudo ss -ltnp 'sport = :9000'
ss -tano 'sport = :9000' | head -4
```

### The fix for your own server

```sh
# ana@greenhouse:~/greenhouse$
python3 collector.py
python3 collector.py
ss -tan 'sport = :9000' | head -3
# ana@greenhouse:~/greenhouse$
python3 collector.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
