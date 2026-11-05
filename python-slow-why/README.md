# Why Python Is Slow (and When It Doesn't Matter)

Video: https://youtu.be/YrXYRiVGork  
Written version: https://cloudexplainers.com/why-python-is-slow-and-when-it-doesn-t-matter/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/builtin.py`](lab/builtin.py)
- [`lab/bytecode.py`](lab/bytecode.py)
- [`lab/loop.c`](lab/loop.c)
- [`lab/loop.py`](lab/loop.py)
- [`lab/numpy_sum.py`](lab/numpy_sum.py)
- [`lab/sizes.py`](lab/sizes.py)
- [`lab/threads.py`](lab/threads.py)
- [`lab/web_request.py`](lab/web_request.py)

## Commands, in the order the video runs them

### The problem

```sh
# ana@laptop:~/shop$
python3 loop.py
gcc -O2 -o loop loop.c
./loop
```

### Reason 1: the interpreter

```sh
# ana@laptop:~/shop$
python3 bytecode.py
```

### Reason 2: everything is an object

```sh
# ana@laptop:~/shop$
python3 sizes.py
```

### Reason 3: the GIL

```sh
# ana@laptop:~/shop$
python3 threads.py
```

### How Python code goes fast

```sh
# ana@laptop:~/shop$
python3 builtin.py
python3 numpy_sum.py
pypy3 loop.py
```

### When it doesn't matter

```sh
# ana@laptop:~/shop$
python3 web_request.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
