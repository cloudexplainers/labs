# OpenRouter Will Finally Make Sense After This

Video: https://youtu.be/UcAV6u1p8bk  
Written version: https://cloudexplainers.com/openrouter-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/ask`](lab/shop/ask)
- [`lab/shop/cost`](lab/shop/cost)
- [`lab/shop/describe.py`](lab/shop/describe.py)
- [`lab/shop/describe_openai.py`](lab/shop/describe_openai.py)
- [`lab/shop/doc`](lab/shop/doc)
- [`lab/shop/providers`](lab/shop/providers)
- [`lab/shop/usage`](lab/shop/usage)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### The first free request

```sh
# ana@laptop:~/shop$
./ask google/gemma-4-31b-it:free
jq -r '.error.metadata | .raw, .provider_name, .limit_source' reply.json | cut -d. -f1
```

### What OpenRouter is

```sh
# ana@laptop:~/shop$
curl -s https://openrouter.ai/api/v1/models | jq '.data | length'
curl -s https://openrouter.ai/api/v1/models | jq '[.data[].id | split("/")[0]] | unique | length'
curl -s https://openrouter.ai/api/v1/models | jq -r '.data[].id | select(endswith(":free"))'
```

### One request, end to end

```sh
# ana@laptop:~/shop$
cat ask
./ask nvidia/nemotron-3.5-lightning:free
./cost
```

### A model is not a provider

```sh
# ana@laptop:~/shop$
./providers google/gemma-4-31b-it
./providers google/gemma-4-31b-it:free
```

### What changes in your code

```sh
# ana@laptop:~/shop$
diff describe_openai.py describe.py
python describe.py cohere/north-mini-code:free
```

### What free really means

```sh
# ana@laptop:~/shop$
./usage
./ask anthropic/claude-haiku-5.5
```

### When a model is busy

```sh
# ana@laptop:~/shop$
./ask google/gemma-4-31b-it:free nvidia/nemotron-3.5-lightning:free
./ask openrouter/free
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
