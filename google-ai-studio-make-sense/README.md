# Google AI Studio Will Finally Make Sense After This

Video: https://youtu.be/j7BVIQWSzYA  
Written version: https://cloudexplainers.com/google-ai-studio-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/ask`](lab/shop/ask)
- [`lab/shop/card.json`](lab/shop/card.json)
- [`lab/shop/describe.py`](lab/shop/describe.py)
- [`lab/shop/low.json`](lab/shop/low.json)
- [`lab/shop/plain.json`](lab/shop/plain.json)
- [`lab/shop/system.json`](lab/shop/system.json)
- [`lab/shop/temp0.json`](lab/shop/temp0.json)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### What AI Studio really is

```sh
# ana@laptop:~/shop$
echo ${#GEMINI_API_KEY}
API=https://generativelanguage.googleapis.com/v1beta
curl -s -H "x-goog-api-key: $GEMINI_API_KEY" "$API/models?pageSize=200" | jq '.models | length'
curl -s -H "x-goog-api-key: $GEMINI_API_KEY" "$API/models?pageSize=200" | jq -r '.models[].name' | grep -E 'gemini-3\.[5-8]-flash$'
```

### One prompt, one request

```sh
# ana@laptop:~/shop$
cat plain.json
cat ask
./ask plain.json > reply.txt
wc -w reply.txt
head -3 reply.txt
tail -1 reply.txt
```

### The settings, one field each

```sh
# ana@laptop:~/shop$
cat system.json
./ask system.json
diff system.json low.json
./ask low.json
diff low.json temp0.json
./ask temp0.json
./ask temp0.json
```

### From playground to code

```sh
# ana@laptop:~/shop$
cat card.json
./ask card.json > card.txt
cat card.txt
head -1 card.txt | jq .price_eur
cat describe.py
source ~/.venv/bin/activate
# (.venv) ana@laptop:~/shop$
python describe.py
env -u GEMINI_API_KEY python describe.py 2>&1 | tail -1
```

### Free tier, limits and your data

```sh
# ana@laptop:~/shop$
GEMINI_API_KEY=$FREE_KEY ./ask low.json
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
