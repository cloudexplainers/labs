# How RAG Works

Video: https://youtu.be/Enuw0MGjunE  
Written version: https://cloudexplainers.com/how-rag-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/docs/hours.md`](lab/docs/hours.md)
- [`lab/docs/keys.md`](lab/docs/keys.md)
- [`lab/docs/paint.md`](lab/docs/paint.md)
- [`lab/docs/rentals.md`](lab/docs/rentals.md)
- [`lab/docs/returns.md`](lab/docs/returns.md)
- [`lab/helpdesk.py`](lab/helpdesk.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Made up

```sh
ask "What is the restocking fee on an opened drill?"
# kari@shop:~/helpdesk$
grep -i restocking docs/*.md
```

### Chunk

```sh
# kari@shop:~/helpdesk$
ls docs
chunk
```

### Embed

```sh
embed "opened drill"
# kari@shop:~/helpdesk$
similar "return a drill" "bring back a power tool"
similar "return a drill" "rent a tile saw"
index
ls -lh index.json
```

### Search

```sh
search "What is the restocking fee on an opened drill?"
# kari@shop:~/helpdesk$
grep -ic "bring back" docs/*.md
search "Can I bring back a sander I already opened?"
```

### Augment and generate

```sh
rag --show "What is the restocking fee on an opened drill?"
# kari@shop:~/helpdesk$
rag "Do you rent kayaks?"
```

### The stale index

```sh
# kari@shop:~/helpdesk$
tail -n 2 docs/returns.md
rag --show "Got a ladder as a gift Dec 10. Return it Jan 20?"
# kari@shop:~/helpdesk$
index
rag --show "Got a ladder as a gift Dec 10. Return it Jan 20?"
```

### Saturday

```sh
# kari@shop:~/helpdesk$
rag "Can I bring back a sander I already opened?"
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
