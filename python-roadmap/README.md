# The Python Roadmap for Beginners

Video: https://youtu.be/dYPUyr3fxIU  
Written version: https://cloudexplainers.com/the-python-roadmap-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/files/hello.py`](lab/files/hello.py)
- [`lab/files/orders.csv`](lab/files/orders.csv)
- [`lab/files/test_totals.py`](lab/files/test_totals.py)
- [`lab/files/totals_v1.py`](lab/files/totals_v1.py)
- [`lab/files/totals_v2.py`](lab/files/totals_v2.py)
- [`lab/files/totals_v3.py`](lab/files/totals_v3.py)
- [`lab/files/totals_v4.py`](lab/files/totals_v4.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Where beginners get stuck

```sh
# ana@bakery:~/orders$
python
python3 totals.py
pip install openpyxl
```

### Stage 1: run Python

```sh
# ana@bakery:~/orders$
python3 --version
python3
>>> 2 + 3
>>> print("Good morning")
# ana@bakery:~/orders$
cat hello.py
python3 hello.py
```

### Stage 2: the basics

```sh
# ana@bakery:~/orders$
python3
>>> qty = "3"
>>> type(qty)
>>> qty * 2
>>> int(qty) * 2
>>> items = ["rye loaf", "croissant", "sourdough"]
>>> len(items)
>>> prices = {"rye loaf": 4.50, "croissant": 2.20}
>>> prices["croissant"]
```

### Stage 3: errors and files

```sh
# ana@bakery:~/orders$
cat orders.csv
cat totals.py
grep qty totals.py
python3 totals.py
python3 totals.py
```

### Stage 4: packages

```sh
# ana@bakery:~/orders$
head -n 3 totals.py
python3 totals.py
python3 -m venv .venv
source .venv/bin/activate
# (.venv) ana@bakery:~/orders$
which python
pip install openpyxl
python3 totals.py
pip freeze > requirements.txt
cat requirements.txt
```

### Stage 6: tests and Git

```sh
# (.venv) ana@bakery:~/orders$
cat test_totals.py
pip install pytest
pytest -q
python3
>>> 3 * 1.10
>>> round(3 * 1.10, 2)
# (.venv) ana@bakery:~/orders$
grep round totals.py
pytest -q
echo .venv > .gitignore
git init -q
git add .
git commit -q -m "Order report with tests"
git log --oneline
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
