# How to Fix Python cron Jobs That Never Run

Video: https://youtu.be/ZIym0xc1Pjs  
Written version: https://cloudexplainers.com/how-to-fix-python-cron-jobs-that-never-run/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/bikes.env`](lab/bikes.env)
- [`lab/bikes/rentals.csv`](lab/bikes/rentals.csv)
- [`lab/bikes/report.py`](lab/bikes/report.py)
- [`lab/capture.py`](lab/capture.py)
- [`lab/dashboard/app.py`](lab/dashboard/app.py)
- [`lab/dashboard/dashboard.service`](lab/dashboard/dashboard.service)
- [`lab/v2/report.py`](lab/v2/report.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Works by hand, not from cron

```sh
# (.venv) ana@bikes:~/bikes$
python report.py
crontab -l
```

### Did cron even start it?

```sh
# (.venv) ana@bikes:~/bikes$
journalctl -u cron --since "3 minutes ago" --no-pager
crontab crontab.txt
crontab -l
cat cron.log
```

### Missing 1: which Python?

```sh
# (.venv) ana@bikes:~/bikes$
which python
deactivate
# ana@bikes:~/bikes$
which python3
python3 report.py
```

### Missing 2: which folder?

```sh
# ana@bikes:~/bikes$
tail -n 5 cron.log
crontab -l
cat ~/cron-folder.txt
grep -n "HERE" report.py
```

### Missing 3: which variables?

```sh
# ana@bikes:~/bikes$
tail -n 6 cron.log
grep BIKES ~/.bashrc
cat ~/cron-env.txt
cat crontab.txt
crontab crontab.txt
crontab -l
cat crontab.txt
crontab crontab.txt
tail -n 1 cron.log
```

### When it truly never starts

```sh
# ana@bikes:~/bikes$
systemctl is-active cron
date
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
