# How to Fix Python pip error: externally-managed-environment

Video: https://youtu.be/St4Kf_abJyU  
Written version: https://cloudexplainers.com/how-to-fix-python-pip-error-externally-managed-environment/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/prices.json`](lab/prices.json)
- [`lab/prices.py`](lab/prices.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### externally-managed-environment

```sh
# ana@laptop:~/prices$
pip install requests
python3 prices.py
```

### Why pip says no

```sh
# ana@laptop:~/prices$
ls /usr/lib/python3.12/EXTERNALLY-MANAGED
dpkg -S /usr/lib/python3.12/EXTERNALLY-MANAGED
dpkg -S /usr/lib/python3/dist-packages
head -1 /usr/bin/add-apt-repository
```

### The apt package

```sh
# ana@laptop:~/prices$
sudo apt install -y python3-requests
python3 prices.py
apt list --installed python3-requests
```

### A virtual environment

```sh
# ana@laptop:~/prices$
python3 -m venv .venv
sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
# (.venv) ana@laptop:~/prices$
which python pip
pip install requests
python prices.py
pip freeze > requirements.txt
cat requirements.txt
deactivate
# ana@laptop:~/prices$
python3 -c 'import requests; print(requests.__version__)'
```

### pipx for apps

```sh
# ana@laptop:~/prices$
sudo apt install -y pipx
pipx install httpie
pipx ensurepath
http localhost:8000/prices.json
```

### Forcing it

```sh
# ana@laptop:~/prices$
sudo pip install --break-system-packages --upgrade requests
python3 -c 'import requests; print(requests.__version__, requests.__file__)'
sudo pip uninstall -y --break-system-packages requests
python3 -c 'import requests; print(requests.__version__, requests.__file__)'
apt list --installed python3-requests
dpkg --verify python3-requests | head -4
sudo apt install --reinstall -y python3-requests
python3 -c 'import requests; print(requests.__version__, requests.__file__)'
```

### Keep it from coming back

```sh
# ana@laptop:~/prices$
rm -rf .venv
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python prices.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
