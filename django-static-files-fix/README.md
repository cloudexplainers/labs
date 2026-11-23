# How to Fix Django Static Files Not Loading in Production

Video: https://youtu.be/DjJ2PcMT1Po  
Written version: https://cloudexplainers.com/how-to-fix-django-static-files-not-loading-in-production/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/capture.py`](lab/capture.py)
- [`lab/tractors/manage.py`](lab/tractors/manage.py)
- [`lab/tractors/showroom/__init__.py`](lab/tractors/showroom/__init__.py)
- [`lab/tractors/showroom/apps.py`](lab/tractors/showroom/apps.py)
- [`lab/tractors/showroom/templates/showroom/home.html`](lab/tractors/showroom/templates/showroom/home.html)
- [`lab/tractors/showroom/views.py`](lab/tractors/showroom/views.py)
- [`lab/tractors/static/css/site.css`](lab/tractors/static/css/site.css)
- [`lab/tractors/static/img/field-star.svg`](lab/tractors/static/img/field-star.svg)
- [`lab/tractors/static/img/hill-hauler.svg`](lab/tractors/static/img/hill-hauler.svg)
- [`lab/tractors/static/img/logo.svg`](lab/tractors/static/img/logo.svg)
- [`lab/tractors/static/img/orchard-mini.svg`](lab/tractors/static/img/orchard-mini.svg)
- [`lab/tractors/tractors/__init__.py`](lab/tractors/tractors/__init__.py)
- [`lab/tractors/tractors/settings.py`](lab/tractors/tractors/settings.py)
- [`lab/tractors/tractors/urls.py`](lab/tractors/tractors/urls.py)
- [`lab/tractors/tractors/wsgi.py`](lab/tractors/tractors/wsgi.py)
- [`lab/v2/compact-30.svg`](lab/v2/compact-30.svg)
- [`lab/v2/views.py`](lab/v2/views.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### The usual fix: three parts

```sh
# (.venv) ana@dealership:~/tractors$
curl -s localhost | grep -n static
curl -sI localhost/static/css/site.css | head -n 1
```

### Turning DEBUG on isn't the fix

```sh
# (.venv) ana@dealership:~/tractors$
grep -n DEBUG tractors/settings.py
grep -n DEBUG tractors/settings.py
sudo systemctl restart tractors
curl -sI localhost/static/css/site.css | head -n 1
```

### No STATIC_ROOT: collectstatic refuses

```sh
# (.venv) ana@dealership:~/tractors$
python manage.py collectstatic
grep -n STATIC tractors/settings.py
python manage.py collectstatic --noinput
ls staticfiles
```

### nginx sends /static/ to Django

```sh
# (.venv) ana@dealership:~/tractors$
curl -sI localhost/static/css/site.css | head -n 1
grep -n location /etc/nginx/sites-available/tractors
grep -n -A 2 'location /static/' /etc/nginx/sites-available/tractors
sudo nginx -t
sudo systemctl reload nginx
curl -sI localhost/static/css/site.css | head -n 1
sudo tail -n 1 /var/log/nginx/error.log
ps -o user= -C nginx | sort | uniq -c
ls -ld /home/ana
```

### Permission denied: nginx can't read a home folder

```sh
# (.venv) ana@dealership:~/tractors$
sudo mkdir -p /var/www/tractors && sudo chown ana:ana /var/www/tractors
grep -n STATIC_ROOT tractors/settings.py
python manage.py collectstatic --noinput
grep -n alias /etc/nginx/sites-available/tractors
sudo nginx -t
sudo systemctl reload nginx
curl -sI localhost/static/css/site.css | head -n 1
```

### An alias without its last slash

```sh
# (.venv) ana@dealership:~/tractors$
sudo tail -n 1 /var/log/nginx/error.log
grep -n alias /etc/nginx/sites-available/tractors
sudo nginx -t
sudo systemctl reload nginx
curl -sI localhost/static/css/site.css | head -n 1
```

### A new photo: collect on every deploy

```sh
# (.venv) ana@dealership:~/tractors$
curl -sI localhost/static/img/compact-30.svg | head -n 1
python manage.py collectstatic --noinput
curl -sI localhost/static/img/compact-30.svg | head -n 1
```

### No nginx? WhiteNoise

```sh
# (.venv) ana@dealership:~/tractors$
curl -sI localhost:8000/static/css/site.css | head -n 1
grep -n -i whitenoise tractors/settings.py
sudo systemctl restart tractors
curl -sI localhost:8000/static/css/site.css | head -n 1
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
