# Why OpenRouter Free Models Hit Their Limit So Fast

Video: https://youtu.be/72fAhHf_074  
Written version: https://cloudexplainers.com/why-openrouter-free-models-hit-their-limit-so-fast/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/ask`](lab/shop/ask)
- [`lab/shop/burst`](lab/shop/burst)
- [`lab/shop/doc`](lab/shop/doc)
- [`lab/shop/usage`](lab/shop/usage)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Every free request: 429

```sh
# ana@laptop:~/shop$
./ask nvidia/nemotron-3.5-lightning:free
./ask cohere/north-mini-code:free
```

### Why fifty goes so fast

```sh
# ana@laptop:~/shop$
cat burst
./burst 22 nvidia/nemotron-3.5-lightning:free
./usage
./burst 29 nvidia/nemotron-3.5-lightning:free
```

### The counter runs behind

```sh
# ana@laptop:~/shop$
./usage
```

### When it comes back

```sh
# ana@laptop:~/shop$
date -u -d @$(( $(grep -i '^x-ratelimit-reset' headers.txt | tr -dc 0-9) / 1000 ))
date -u
./usage
./ask nvidia/nemotron-3.5-lightning:free
./usage
./usage
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
