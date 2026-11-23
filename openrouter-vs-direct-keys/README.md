# OpenRouter vs Direct API Keys: Which One Should You Use?

Video: https://youtu.be/axQNrOg8eAs  
Written version: https://cloudexplainers.com/openrouter-vs-direct-api-keys-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/grocery/doc`](lab/grocery/doc)
- [`lab/grocery/google.env`](lab/grocery/google.env)
- [`lab/grocery/list.txt`](lab/grocery/list.txt)
- [`lab/grocery/providers`](lab/grocery/providers)
- [`lab/grocery/router.env`](lab/grocery/router.env)
- [`lab/grocery/sort.py`](lab/grocery/sort.py)
- [`lab/grocery/usage`](lab/grocery/usage)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### One model, two keys

```sh
# kari@laptop:~/grocery$
python sort.py google
python sort.py router
```

### Two doors to the same model

```sh
# kari@laptop:~/grocery$
./providers google/gemma-4-26b-a4b-it:free
./providers google/gemma-4-26b-a4b-it
```

### One key, every company

```sh
# kari@laptop:~/grocery$
MODEL=nvidia/nemotron-3.5-lightning:free python sort.py router
MODEL=nvidia/nemotron-3.5-lightning:free python sort.py google
MODEL=google/gemma-4-26b-a4b-it:free,nvidia/nemotron-3.5-lightning:free python sort.py router
```

### What only the maker gives you

```sh
# kari@laptop:~/grocery$
MODEL=gemini-3.6-flash python sort.py google
MODEL=google/gemini-3.6-flash python sort.py router
```

### What it costs

```sh
# kari@laptop:~/grocery$
./usage
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
