# The Django Roadmap for Beginners

Video: https://youtu.be/acqMOtbTj-o  
Written version: https://cloudexplainers.com/the-django-roadmap-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/admin_v1/signups/admin.py`](lab/steps/admin_v1/signups/admin.py)
- [`lab/steps/form_v1/signups/forms.py`](lab/steps/form_v1/signups/forms.py)
- [`lab/steps/form_v1/signups/static/signups/style.css`](lab/steps/form_v1/signups/static/signups/style.css)
- [`lab/steps/form_v1/signups/templates/signups/list.html`](lab/steps/form_v1/signups/templates/signups/list.html)
- [`lab/steps/form_v1/signups/templates/signups/new.html`](lab/steps/form_v1/signups/templates/signups/new.html)
- [`lab/steps/form_v1/signups/urls.py`](lab/steps/form_v1/signups/urls.py)
- [`lab/steps/form_v1/signups/views.py`](lab/steps/form_v1/signups/views.py)
- [`lab/steps/model_v1/signups/models.py`](lab/steps/model_v1/signups/models.py)
- [`lab/steps/model_v1/signups/views.py`](lab/steps/model_v1/signups/views.py)
- [`lab/steps/template_v1/signups/templates/signups/list.html`](lab/steps/template_v1/signups/templates/signups/list.html)
- [`lab/steps/template_v1/signups/views.py`](lab/steps/template_v1/signups/views.py)
- [`lab/steps/test_v1/signups/tests.py`](lab/steps/test_v1/signups/tests.py)
- [`lab/steps/urls_v1/potluck/urls.py`](lab/steps/urls_v1/potluck/urls.py)
- [`lab/steps/urls_v1/signups/urls.py`](lab/steps/urls_v1/signups/urls.py)
- [`lab/steps/urls_v1/signups/views.py`](lab/steps/urls_v1/signups/views.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Works on the laptop, not for real

```sh
# (.venv) dave@laptop:~/potluck$
grep -n '^DEBUG\|^ALLOWED_HOSTS' potluck/settings.py
python manage.py runserver
```

### Stage 1: Python and a venv

```sh
# dave@laptop:~/potluck$
python3 -m venv .venv
source .venv/bin/activate
# (.venv) dave@laptop:~/potluck$
pip install django
django-admin startproject potluck .
ls
python manage.py runserver
```

### Stage 2: URLs and views

```sh
# (.venv) dave@laptop:~/potluck$
python manage.py startapp signups
cat signups/views.py
cat signups/urls.py
curl -s localhost:8000/signups/
curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/signup/
```

### Stage 3: templates

```sh
# (.venv) dave@laptop:~/potluck$
cat signups/templates/signups/list.html
curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/signups/
python manage.py runserver
grep -A8 '^INSTALLED_APPS' potluck/settings.py
curl -s localhost:8000/signups/
```

### Stage 4: models

```sh
# (.venv) dave@laptop:~/potluck$
sed -n '4,9p' signups/models.py
python manage.py makemigrations
curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/signups/
python manage.py runserver
python manage.py migrate
python manage.py shell -c "from signups.models import Dish; Dish.objects.create(name='Lasagna', person='Beth', kind='main'); Dish.objects.create(name='Coleslaw', person='Dave', kind='side'); print(Dish.objects.count(), 'dishes')"
python manage.py shell -c "from signups.models import Dish; print(Dish.objects.filter(kind='main'))"
```

### Stage 6: forms

```sh
# (.venv) dave@laptop:~/potluck$
grep -n 'form\|csrf' signups/templates/signups/new.html
curl -s -o /dev/null -w '%{http_code}\n' -X POST -d 'name=Chili&person=Dave&kind=main' localhost:8000/signups/new/
python manage.py runserver
```

### Stage 7: tests

```sh
# (.venv) dave@laptop:~/potluck$
sed -n '7,10p' signups/tests.py
python manage.py test
```

### Stage 8: real-world settings

```sh
# (.venv) dave@laptop:~/potluck$
grep -n '^DEBUG\|^ALLOWED_HOSTS' potluck/settings.py
curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/signups/
python manage.py check --deploy
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
