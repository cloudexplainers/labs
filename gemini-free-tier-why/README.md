# Why Your Gemini API Free Tier Runs Out So Fast

Video: https://youtu.be/1O2j0HIYn90  
Written version: https://cloudexplainers.com/why-your-gemini-api-free-tier-runs-out-so-fast/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/make_catalog.py`](lab/make_catalog.py)
- [`lab/shop/agent.py`](lab/shop/agent.py)
- [`lab/shop/ask`](lab/shop/ask)
- [`lab/shop/batch.py`](lab/shop/batch.py)
- [`lab/shop/chat.py`](lab/shop/chat.py)
- [`lab/shop/describe.py`](lab/shop/describe.py)
- [`lab/shop/teas.txt`](lab/shop/teas.txt)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Out after a handful

```sh
# ana@laptop:~/shop$
python describe.py
jq -r .error.message error.json
```

### How small the free tier is

```sh
# ana@laptop:~/shop$
sed -n 5,19p describe.py
```

### One question, many requests

```sh
# ana@laptop:~/shop$
sed -n 10,21p agent.py
sed -n 5,8p agent.py
python agent.py 2>/dev/null
```

### Tokens run out first

```sh
# ana@laptop:~/shop$
wc -l catalog.txt && head -3 catalog.txt
sed -n 5,13p chat.py
python chat.py
```

### Make it last

```sh
# ana@laptop:~/shop$
sed -n 16,21p batch.py
MODEL=gemini-3.5-flash-lite python batch.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
