# Every Django Concept a Beginner Needs to Know

Video: https://youtu.be/Go_7URlZlDk  
Written version: https://cloudexplainers.com/every-django-concept-a-beginner-needs-to-know/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/steps/seed.py`](lab/steps/seed.py)
- [`lab/steps/v1/jobs/admin.py`](lab/steps/v1/jobs/admin.py)
- [`lab/steps/v1/jobs/forms.py`](lab/steps/v1/jobs/forms.py)
- [`lab/steps/v1/jobs/middleware.py`](lab/steps/v1/jobs/middleware.py)
- [`lab/steps/v1/jobs/models.py`](lab/steps/v1/jobs/models.py)
- [`lab/steps/v1/jobs/templates/jobs/base.html`](lab/steps/v1/jobs/templates/jobs/base.html)
- [`lab/steps/v1/jobs/templates/jobs/job.html`](lab/steps/v1/jobs/templates/jobs/job.html)
- [`lab/steps/v1/jobs/templates/jobs/open.html`](lab/steps/v1/jobs/templates/jobs/open.html)
- [`lab/steps/v1/jobs/templates/registration/login.html`](lab/steps/v1/jobs/templates/registration/login.html)
- [`lab/steps/v1/jobs/urls.py`](lab/steps/v1/jobs/urls.py)
- [`lab/steps/v1/jobs/views.py`](lab/steps/v1/jobs/views.py)
- [`lab/steps/v1/renovate/urls.py`](lab/steps/v1/renovate/urls.py)
- [`lab/steps/v2/jobs/models.py`](lab/steps/v2/jobs/models.py)
- [`lab/steps/v2/jobs/templates/jobs/mine.html`](lab/steps/v2/jobs/templates/jobs/mine.html)
- [`lab/steps/v2/jobs/urls.py`](lab/steps/v2/jobs/urls.py)
- [`lab/steps/v2/jobs/views.py`](lab/steps/v2/jobs/views.py)
- [`lab/steps/v3/jobs/views.py`](lab/steps/v3/jobs/views.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One page, 21 questions

```sh
# (.venv) ben@laptop:~/renovate$
curl -sI localhost:8000/tasks/open/
```

### Project and apps

```sh
# (.venv) ben@laptop:~/renovate$
django-admin startproject renovate .
python manage.py startapp jobs
ls renovate
ls jobs
```

### Settings

```sh
# (.venv) ben@laptop:~/renovate$
grep -n '^DEBUG\|^INSTALLED_APPS\|^DATABASES\|^MIDDLEWARE\|^LOGIN' renovate/settings.py
grep -A8 '^INSTALLED_APPS' renovate/settings.py
```

### URLs

```sh
# (.venv) ben@laptop:~/renovate$
sed -n '/^urlpatterns/,$p' renovate/urls.py
```

### Views

```sh
# (.venv) ben@laptop:~/renovate$
sed -n '/^def job_detail/,/^$/p' jobs/views.py
curl -s -o /dev/null -w '%{http_code}\n' localhost:8000/jobs/99/
curl -s localhost:8000/jobs/99/ | grep -o 'No Job matches the given query.'
curl -s localhost:8000/jobs/abc/ | grep -o 'didn.t match any of these'
```

### Templates

```sh
# (.venv) ben@laptop:~/renovate$
grep -h 'extends\|block content\|{{ task' jobs/templates/jobs/{base,open}.html
```

### Models

```sh
# (.venv) ben@laptop:~/renovate$
sed -n '4,20p' jobs/models.py
```

### Migrations

```sh
# (.venv) ben@laptop:~/renovate$
python manage.py makemigrations
python manage.py sqlmigrate jobs 0001
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations jobs
```

### QuerySets

```sh
# (.venv) ben@laptop:~/renovate$
python manage.py shell
>>> from django.db import connection
>>> tasks = Task.objects.filter(done=False)
>>> len(connection.queries)
>>> tasks.count()
>>> len(connection.queries)
>>> print(tasks.query)
>>> tasks.filter(room='Kitchen').count()
>>> Job.objects.get(pk=99)
# (.venv) ben@laptop:~/renovate$
grep -n 'task.job.address' jobs/templates/jobs/open.html
curl -sI localhost:8000/tasks/open/ | grep -i x-queries
curl -s localhost:8000/tasks/open/ | grep -c '<li>'
```

### The admin

```sh
# (.venv) ben@laptop:~/renovate$
sed -n '3,$p' jobs/admin.py
```

### Forms

```sh
>>> form = TaskForm(data={'room': 'Bathroom', 'title': '   '})
>>> form.is_valid()
>>> form.errors
```

### Middleware

```sh
# (.venv) ben@laptop:~/renovate$
grep -A9 '^MIDDLEWARE' renovate/settings.py
cat jobs/middleware.py
```

### Users and sessions

```sh
# (.venv) ben@laptop:~/renovate$
curl -sI localhost:8000/mine/ | grep -i '^HTTP\|^location'
>>> Session.objects.count()
>>> Session.objects.first().get_decoded()['_auth_user_id']
>>> User.objects.get(username='ana').pk
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
