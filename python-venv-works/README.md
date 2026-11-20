# How Python Virtual Environments Work

Video: https://youtu.be/NYGBE6k_5iI  
Written version: https://cloudexplainers.com/how-python-virtual-environments-work/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/hive-log/weigh.py`](lab/hive-log/weigh.py)
- [`lab/honey-chart/labels.py`](lab/honey-chart/labels.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Installed, then not found

```sh
# ana@laptop:~/hive-log$
python3 -m venv .venv
source .venv/bin/activate
# (.venv) ana@laptop:~/hive-log$
pip install numpy==1.26.4
python weigh.py
# ana@laptop:~/hive-log$
python3 weigh.py
```

### Two Pythons

```sh
# (.venv) ana@laptop:~/hive-log$
which python
# ana@laptop:~/hive-log$
which python3
# (.venv) ana@laptop:~/hive-log$
pip show numpy | grep Location
```

### Inside the .venv folder

```sh
# (.venv) ana@laptop:~/hive-log$
ls .venv
stat -c '%N' .venv/bin/python*
cat .venv/pyvenv.cfg
ls .venv/bin
ls .venv/lib/python3.12/site-packages
du -sh .venv /usr/lib/python3.12
```

### How Python finds its packages

```sh
# ana@laptop:~/hive-log$
python3 -c 'import sys; print(sys.prefix)'
.venv/bin/python -c 'import sys; print(sys.prefix)'
.venv/bin/python weigh.py
```

### What activate really does

```sh
# ana@laptop:~/hive-log$
env | grep -v ^PS1= | sort > /tmp/before; source .venv/bin/activate; env | grep -v ^PS1= | sort > /tmp/after
# (.venv) ana@laptop:~/hive-log$
diff /tmp/before /tmp/after
which python
deactivate; which python3
# ana@laptop:~/hive-log$
python3 -c 'import yaml; print(yaml.__file__)'
# (.venv) ana@laptop:~/hive-log$
python -c 'import yaml'
```

### Two projects, one environment

```sh
# (.venv) ana@laptop:~/hive-log$
cd ~/honey-chart
# (.venv) ana@laptop:~/honey-chart$
python labels.py
pip install --upgrade numpy
python labels.py
python ~/hive-log/weigh.py
# ana@laptop:~/honey-chart$
python3 -m venv .venv && source .venv/bin/activate
# (.venv) ana@laptop:~/honey-chart$
pip install numpy
# ana@laptop:~/hive-log$
source .venv/bin/activate && pip install numpy==1.26.4
# (.venv) ana@laptop:~/honey-chart$
pip list
# (.venv) ana@laptop:~/hive-log$
pip list
python weigh.py
```

### Why a moved venv breaks

```sh
# (.venv) ana@laptop:~/hive-log$
pip freeze > requirements.txt; cat requirements.txt
deactivate; cd ~; mv hive-log hives; cd hives
# ana@laptop:~/hives$
.venv/bin/pip install pyyaml
rm -rf .venv; python3 -m venv .venv; .venv/bin/pip install -r requirements.txt
.venv/bin/python weigh.py
head -1 .venv/bin/pip
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
