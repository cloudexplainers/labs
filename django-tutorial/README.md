# Django Full Tutorial for Beginners

Video: https://youtu.be/EuN2ndLuLvs  
Written version: https://cloudexplainers.com/django-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/s1/config/urls.py`](lab/s1/config/urls.py)
- [`lab/s1/shop/urls.py`](lab/s1/shop/urls.py)
- [`lab/s1/shop/views.py`](lab/s1/shop/views.py)
- [`lab/s2/shop/models.py`](lab/s2/shop/models.py)
- [`lab/s2/shop/templates/shop/base.html`](lab/s2/shop/templates/shop/base.html)
- [`lab/s2/shop/templates/shop/tea_list.html`](lab/s2/shop/templates/shop/tea_list.html)
- [`lab/s2/shop/urls.py`](lab/s2/shop/urls.py)
- [`lab/s2/shop/views.py`](lab/s2/shop/views.py)
- [`lab/s3/shop/admin.py`](lab/s3/shop/admin.py)
- [`lab/s4/shop/templates/shop/tea_detail.html`](lab/s4/shop/templates/shop/tea_detail.html)
- [`lab/s4/shop/templates/shop/tea_list.html`](lab/s4/shop/templates/shop/tea_list.html)
- [`lab/s4/shop/urls.py`](lab/s4/shop/urls.py)
- [`lab/s4/shop/views.py`](lab/s4/shop/views.py)
- [`lab/s5/shop/forms.py`](lab/s5/shop/forms.py)
- [`lab/s5/shop/models.py`](lab/s5/shop/models.py)
- [`lab/s5/shop/templates/shop/order.html`](lab/s5/shop/templates/shop/order.html)
- [`lab/s5/shop/urls.py`](lab/s5/shop/urls.py)
- [`lab/s5/shop/views.py`](lab/s5/shop/views.py)
- [`lab/s6/shop/tests.py`](lab/s6/shop/tests.py)
- [`lab/s7/shop/views.py`](lab/s7/shop/views.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Your first Django site

```sh
# ana@laptop:~/teashop$
tree -I .venv
w3m -dump http://localhost:8000/teas/sencha/
uv run manage.py test
```

### Set up the project

```sh
# ana@laptop:~$
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv init --bare teashop
cd teashop
# ana@laptop:~/teashop$
uv add django
uv run django-admin startproject config .
uv run manage.py runserver
w3m -dump http://localhost:8000 | head -n 6
```

### Apps, views and URLs

```sh
# ana@laptop:~/teashop$
uv run manage.py startapp shop
tree shop
grep -A 8 "^INSTALLED_APPS" config/settings.py
cat shop/views.py
cat shop/urls.py
cat config/urls.py
w3m -dump http://localhost:8000
w3m -dump http://localhost:8000/teas/ | head -n 12
```

### Models and migrations

```sh
# ana@laptop:~/teashop$
cat shop/models.py
cat shop/views.py
cat shop/templates/shop/tea_list.html
cat shop/templates/shop/base.html
curl -s -o /dev/null -w "%{http_code}\n" localhost:8000
uv run manage.py makemigrations
uv run manage.py sqlmigrate shop 0001
cat shop/migrations/0001_initial.py
uv run manage.py migrate
w3m -dump http://localhost:8000
```

### The ORM in the shell

```sh
# ana@laptop:~/teashop$
uv run manage.py shell
>>> Tea.objects.create(name="Sencha", slug="sencha", price="12.50", stock=40)
>>> Tea.objects.create(name="Earl Grey", slug="earl-grey", price="9.00", stock=25)
>>> Tea.objects.create(name="Jasmine Pearls", slug="jasmine-pearls", price="18.00", stock=3)
>>> Tea.objects.create(name="Rooibos", slug="rooibos", price="7.50", stock=60)
>>> Tea.objects.count()
>>> Tea.objects.filter(price__lt=10)
>>> print(Tea.objects.filter(price__lt=10).query)
>>> tea = Tea.objects.get(slug="sencha")
>>> tea.price
>>> tea.stock = 38; tea.save()
>>> Tea.objects.get(slug="matcha")
>>> exit()
# ana@laptop:~/teashop$
w3m -dump http://localhost:8000
```

### The admin site

```sh
# ana@laptop:~/teashop$
cat shop/admin.py
uv run manage.py createsuperuser
curl -sI localhost:8000/admin/ | grep -E "HTTP|Location"
w3m -dump http://localhost:8000/admin/
```

### A page for every tea

```sh
# ana@laptop:~/teashop$
cat shop/urls.py
tail -n 3 shop/views.py
cat shop/templates/shop/tea_detail.html
curl -s -o /dev/null -w "%{http_code}\n" localhost:8000/teas/matcha/
```

### Forms and CSRF

```sh
# ana@laptop:~/teashop$
tail -n 5 shop/models.py
uv run manage.py makemigrations
uv run manage.py migrate
cat shop/forms.py
tail -n 15 shop/views.py
cat shop/templates/shop/order.html
w3m -dump http://localhost:8000/teas/sencha/order/
curl -s localhost:8000/teas/sencha/order/ | grep csrf
D="quantity=2&email=sam@example.com"
curl -s -o /dev/null -w "%{http_code}\n" -d "$D" localhost:8000/teas/sencha/order/
curl -s -c jar.txt -o /dev/null localhost:8000/teas/sencha/order/
T=$(awk '/csrftoken/ {print $7}' jar.txt)
curl -si -b jar.txt -d "$D&csrfmiddlewaretoken=$T" localhost:8000/teas/sencha/order/ | grep -E "HTTP|Loc"
curl -s -b jar.txt -d "quantity=0&email=sam&csrfmiddlewaretoken=$T" localhost:8000/teas/sencha/order/ | w3m -dump -T text/html
uv run manage.py shell -c "print(Order.objects.count())"
```

### Tests catch a bug

```sh
# ana@laptop:~/teashop$
head -n 17 shop/tests.py
tail -n +18 shop/tests.py
uv run manage.py test
grep -A 10 "def order" shop/views.py
curl -s -b jar.txt -d "quantity=5&email=sam@example.com&csrfmiddlewaretoken=$T" localhost:8000/teas/jasmine-pearls/order/ | w3m -dump -T text/html
```

### Before you go live

```sh
# ana@laptop:~/teashop$
uv run manage.py check --deploy
uv run manage.py runserver
grep -n -E "^(DEBUG|ALLOWED_HOSTS)" config/settings.py
w3m -dump http://localhost:8000/teas/matcha/
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
