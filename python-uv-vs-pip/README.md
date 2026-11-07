# Python uv vs pip: Which One Should You Use?

Video: https://youtu.be/mSGSTPkgP0w  
Written version: https://cloudexplainers.com/python-uv-vs-pip-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/app.py`](lab/app.py)
- [`lab/prices.json`](lab/prices.json)
- [`lab/requirements.txt`](lab/requirements.txt)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### uv or pip?

```sh
# ana@laptop:~/shop$
cat requirements.txt
time (python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt)
rm -rf .venv && time (uv venv -q && uv pip install -r requirements.txt)
```

### Two tools

```sh
# ana@laptop:~/shop$
pip --version
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv --version
```

### The race

```sh
# ana@laptop:~/shop$
rm -rf .venv && time (python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt)
rm -rf .venv && time (uv venv -q && uv pip install -r requirements.txt)
```

### Why uv is faster

```sh
# ana@laptop:~/shop$
stat -c '%h links: %n' .venv/lib/python3.12/site-packages/pandas/__init__.py
du -sh ~/.cache/pip ~/.cache/uv
```

### More than an installer

```sh
# ana@laptop:~/shop$
rm -rf .venv && uv init --bare
uv add -r requirements.txt
cat pyproject.toml
grep -c '^name = ' uv.lock
grep -A2 '^name = "pandas"' uv.lock
uv run app.py
uv python install 3.13
uv run --python 3.13 python --version
python3 --version
```

### The trap

```sh
# ana@laptop:~/shop$
source .venv/bin/activate
# (shop) ana@laptop:~/shop$
pip install rich
which pip
python -m pip --version
uv add rich
deactivate
# ana@laptop:~/shop$
cd ~ && uv pip install rich
# ana@laptop:~$
uv venv --seed -q seeded && ls seeded/bin
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
