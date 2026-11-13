# How to Fix nginx 502 Bad Gateway Errors on Linux

Video: https://youtu.be/6didaZWn38A  
Written version: https://cloudexplainers.com/how-to-fix-nginx-502-bad-gateway-errors-on-linux/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/booking/booking.py`](lab/booking/booking.py)
- [`lab/booking/booking.service`](lab/booking/booking.service)
- [`lab/booking/nginx-booking`](lab/booking/nginx-booking)
- [`lab/booking/sessions.csv`](lab/booking/sessions.csv)
- [`lab/capture.py`](lab/capture.py)
- [`lab/v2/booking.py`](lab/v2/booking.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### nginx is running. The page says 502

```sh
# ana@gym:~$
curl -sI localhost | head -n 1
systemctl status nginx --no-pager
sudo systemctl restart nginx
curl -sI localhost | head -n 1
```

### The quick fix: nginx's error log

```sh
# ana@gym:~$
sudo tail -n 1 /var/log/nginx/error.log
curl -I 127.0.0.1:8000
systemctl status booking --no-pager
journalctl -u booking -n 40 --no-pager
grep -n BOOKING_DB /etc/systemd/system/booking.service
sudo systemctl daemon-reload
sudo systemctl restart booking
curl -sI localhost | head -n 1
```

### Refused, but the app is running

```sh
# ana@gym:~$
curl -sI localhost | head -n 1
sudo tail -n 1 /var/log/nginx/error.log
systemctl is-active booking
sudo ss -ltnp | grep gunicorn
grep -n proxy_pass /etc/nginx/sites-available/booking
grep -n proxy_pass /etc/nginx/sites-available/booking
sudo nginx -t
sudo systemctl reload nginx
curl -sI localhost | head -n 1
```

### A slow page: 502 or 504?

```sh
# ana@gym:~$
curl -s -o /dev/null -w '%{http_code} after %{time_total}s\n' localhost/report
sudo tail -n 1 /var/log/nginx/error.log
journalctl -u booking -n 3 --no-pager
grep -n timeout /etc/systemd/system/booking.service
sudo systemctl daemon-reload
sudo systemctl restart booking
curl -s -o /dev/null -w '%{http_code} after %{time_total}s\n' localhost/report
sudo tail -n 1 /var/log/nginx/error.log
grep -n proxy_read_timeout /etc/nginx/sites-available/booking
sudo nginx -t
sudo systemctl reload nginx
curl -s -o /dev/null -w '%{http_code} after %{time_total}s\n' localhost/report
```

### An answer too big for nginx

```sh
# ana@gym:~$
curl -s -o /dev/null -w '%{http_code}\n' localhost/login
sudo tail -n 1 /var/log/nginx/error.log
curl -s -D - -o /dev/null 127.0.0.1:8080/login | wc -c
getconf PAGESIZE
grep -n proxy_buffer /etc/nginx/sites-available/booking
sudo nginx -t
grep -n proxy_buffer /etc/nginx/sites-available/booking
sudo nginx -t
sudo systemctl reload nginx
curl -s -o /dev/null -w '%{http_code}\n' localhost/login
```

### The socket in a home folder

```sh
# ana@gym:~$
curl -sI localhost | head -n 1
sudo tail -n 1 /var/log/nginx/error.log
ls -l /home/ana/booking/booking.sock
ps -o user= -C nginx | sort | uniq -c
ls -ld /home/ana
grep -n -e Runtime -e bind /etc/systemd/system/booking.service
grep -n proxy_pass /etc/nginx/sites-available/booking
sudo systemctl daemon-reload
sudo systemctl restart booking
sudo systemctl reload nginx
ls -ld /run/booking
curl -sI localhost | head -n 1
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
