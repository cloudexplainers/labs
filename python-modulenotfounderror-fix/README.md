# How to Fix Python ModuleNotFoundError: No Module Named

Video: https://youtu.be/VMrnxTFClYM  
Written version: https://cloudexplainers.com/how-to-fix-python-modulenotfounderror-no-module-named/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/make_photos.py`](lab/make_photos.py)
- [`lab/recipe-site/build.py`](lab/recipe-site/build.py)
- [`lab/recipe-site/family/__init__.py`](lab/recipe-site/family/__init__.py)
- [`lab/recipe-site/family/render.py`](lab/recipe-site/family/render.py)
- [`lab/recipe-site/recipes/apple-crumble.yaml`](lab/recipe-site/recipes/apple-crumble.yaml)
- [`lab/recipe-site/recipes/aunt-roses-chili.yaml`](lab/recipe-site/recipes/aunt-roses-chili.yaml)
- [`lab/recipe-site/recipes/chicken-soup.yaml`](lab/recipe-site/recipes/chicken-soup.yaml)
- [`lab/recipe-site/recipes/grandmas-lasagna.yaml`](lab/recipe-site/recipes/grandmas-lasagna.yaml)
- [`lab/recipe-site/recipes/lemon-bars.yaml`](lab/recipe-site/recipes/lemon-bars.yaml)
- [`lab/recipe-site/recipes/sunday-pancakes.yaml`](lab/recipe-site/recipes/sunday-pancakes.yaml)
- [`lab/recipe-site/tools/thumbs.py`](lab/recipe-site/tools/thumbs.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Already installed, still not found

```sh
# (.venv) john@family-pc:~/recipe-site$
pip install pyyaml
./build.py
```

### The script's first line picks another Python

```sh
# (.venv) john@family-pc:~/recipe-site$
head -1 build.py
which python
python build.py
```

### Where import looks

```sh
# (.venv) john@family-pc:~/recipe-site$
python -m site | head -7
/usr/bin/python3 -m site | head -8
python -c 'import sys; print(sys.executable)'
python -m pip install pyyaml
```

### New window: environment not active

```sh
# john@family-pc:~/recipe-site$
python3 build.py
which python3
pip install pyyaml
.venv/bin/python build.py
source .venv/bin/activate && python3 build.py
```

### sudo's own PATH

```sh
# (.venv) john@family-pc:~/recipe-site$
python build.py /var/www/recipes
sudo python3 build.py /var/www/recipes
sudo python3 -c 'import sys; print(sys.executable)'
sudo grep secure_path /etc/sudoers
sudo .venv/bin/python build.py /var/www/recipes
```

### PIL and pillow

```sh
# (.venv) john@family-pc:~/recipe-site$
python tools/thumbs.py
pip install PIL
pip install pillow
pip freeze
```

### Your own module, run from a subfolder

```sh
# (.venv) john@family-pc:~/recipe-site$
python tools/thumbs.py
ls
python -m tools.thumbs
```

### Keep it from coming back

```sh
# (.venv) john@family-pc:~/recipe-site$
python -m pip freeze > requirements.txt; cat requirements.txt
deactivate; rm -rf .venv; python3 -m venv .venv; .venv/bin/python -m pip install -r requirements.txt
# john@family-pc:~/recipe-site$
.venv/bin/python build.py && .venv/bin/python -m tools.thumbs
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
