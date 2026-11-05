# Django vs FastAPI: Which One Should You Use?

Video: https://youtu.be/ImjnA7YUYZo  
Written version: https://cloudexplainers.com/django-vs-fastapi-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/django/admin.py`](lab/django/admin.py)
- [`lab/django/models.py`](lab/django/models.py)
- [`lab/django/teas.json`](lab/django/teas.json)
- [`lab/django/urls.py`](lab/django/urls.py)
- [`lab/django/views.py`](lab/django/views.py)
- [`lab/fastapi/main.py`](lab/fastapi/main.py)
- [`lab/hammer.py`](lab/hammer.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Django: what you get for free

```sh
# (.venv) ana@laptop:~/django-shop$
django-admin startproject teashop .
python manage.py startapp menu
find . -name "*.py" | wc -l
ls . teashop menu
cat menu/models.py
python manage.py makemigrations menu
python manage.py migrate
python manage.py loaddata teas.json
python manage.py createsuperuser
python manage.py runserver
# (.venv) ana@laptop:~$
curl -s localhost:8000/teas/
curl -s localhost:8000/admin/login/ | grep -o "<title>.*</title>"
```

### FastAPI: one small file

```sh
# (.venv) ana@laptop:~/fastapi-shop$
ls
wc -l main.py
cat main.py
uvicorn main:app --port 8001
# (.venv) ana@laptop:~$
curl -s localhost:8001/teas
curl -s localhost:8001/teas -H "Content-Type: application/json" -d '{"name": "Rooibos", "price": 4.5, "stock": 30}'
curl -s -w "\nHTTP %{http_code}\n" localhost:8001/teas -H "Content-Type: application/json" -d '{"name": "Rooibos", "price": "cheap", "stock": 30}'
```

### Which one is faster?

```sh
# (.venv) ana@laptop:~/fastapi-shop$
uvicorn main:app --port 8001 --no-access-log
# (.venv) ana@laptop:~$
python3 hammer.py localhost:8001/supplier 50
# (.venv) ana@laptop:~/fastapi-shop$
sed -i 's/await asyncio.sleep(1)/time.sleep(1)/' main.py
grep -n -A2 "async def supplier" main.py
# (.venv) ana@laptop:~$
python3 hammer.py localhost:8001/supplier 50
# (.venv) ana@laptop:~/fastapi-shop$
sed -i 's/^async def supplier/def supplier/' main.py
grep -n -A2 "def supplier" main.py
# (.venv) ana@laptop:~$
python3 hammer.py localhost:8001/supplier 50
# (.venv) ana@laptop:~/django-shop$
gunicorn teashop.wsgi --workers 4 --bind 127.0.0.1:8000
# (.venv) ana@laptop:~$
python3 hammer.py localhost:8000/supplier/ 50
# (.venv) ana@laptop:~/django-shop$
uvicorn teashop.asgi:application --port 8000 --no-access-log
# (.venv) ana@laptop:~$
python3 hammer.py localhost:8000/supplier-async/ 50
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
