# Gemini API vs Vertex AI: Which One Should You Use?

Video: https://youtu.be/db8pa3RJ9zU  
Written version: https://cloudexplainers.com/gemini-api-vs-vertex-ai-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/shop/ask`](lab/shop/ask)
- [`lab/shop/describe.py`](lab/shop/describe.py)
- [`lab/shop/describe_vertex.py`](lab/shop/describe_vertex.py)
- [`lab/shop/doc`](lab/shop/doc)
- [`lab/shop/get_token.py`](lab/shop/get_token.py)
- [`lab/shop/where.py`](lab/shop/where.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Same model, two doors

```sh
# ana@laptop:~/shop$
python describe.py
./ask vertex --key
```

### The key Vertex AI won't take

```sh
# ana@laptop:~/shop$
cat describe.py
./ask gemini
jq -r .error.message reply.json
```

### How Vertex AI knows who you are

```sh
# ana@laptop:~/shop$
cat describe_vertex.py
python describe_vertex.py 2>&1 | tail -1
./ask vertex
export GOOGLE_APPLICATION_CREDENTIALS=~/keys/shop-bot.json
./ask vertex
jq -r .error.message reply.json | cut -d' ' -f1-4
./ask vertex
./ask vertex
jq -r .error.message reply.json | cut -d. -f1
```

### What changes in your code

```sh
# ana@laptop:~/shop$
diff describe.py describe_vertex.py
python describe_vertex.py
GOOGLE_GENAI_USE_VERTEXAI=true GOOGLE_CLOUD_PROJECT=ce-vertex-p048 GOOGLE_CLOUD_LOCATION=global python describe.py
```

### Where your request runs

```sh
# ana@laptop:~/shop$
cat where.py
python where.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
