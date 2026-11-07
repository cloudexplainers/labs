# How to Fix Gemini API Error 429: Resource Exhausted

Video: https://youtu.be/sGn2F15hwPI  
Written version: https://cloudexplainers.com/how-to-fix-gemini-api-error-429-resource-exhausted/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/ask`](lab/shop/ask)
- [`lab/shop/describe.py`](lab/shop/describe.py)
- [`lab/shop/paced.py`](lab/shop/paced.py)
- [`lab/shop/retry.py`](lab/shop/retry.py)
- [`lab/shop/teas.txt`](lab/shop/teas.txt)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Every request says 429

```sh
# ana@laptop:~/shop$
python describe.py 2>&1 | cut -c1-80
```

### The quick fix

```sh
# ana@laptop:~/shop$
./ask "One calm sentence about Sencha tea."
jq -r .error.message error.json
sleep 25 && ./ask "One calm sentence about Sencha tea."
```

### What 429 is telling you

```sh
# ana@laptop:~/shop$
jq '.error.details[1].violations[0]' error.json
jq '.error.details[2]' error.json
MODEL=gemini-3.1-flash-lite ./ask "One calm sentence about Sencha tea."
```

### When waiting won't help

```sh
# ana@laptop:~/shop$
MODEL=gemini-3.7-flash ./ask "One calm sentence about Sencha tea."
jq -r .error.message error.json
MODEL=gemini-3.1-pro-preview ./ask "One calm sentence about Sencha tea."
jq -r .error.message error.json
GEMINI_API_KEY=$PAID_KEY MODEL=gemini-3.1-pro-preview ./ask "One calm sentence about Sencha tea."
```

### Fix it in your code

```sh
# ana@laptop:~/shop$
sed -n 10,15p retry.py
sed -n 18,31p retry.py
time python retry.py
cat paced.py
time python paced.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
