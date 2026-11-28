#!/usr/bin/env python3
"""Kari's Hardware help desk: a tiny retrieval-augmented generation (RAG) pipeline, standard library only.

One script, installed under several names (ask, chunk, embed, similar, index, search, rag); it talks to Ollama's
HTTP API (OLLAMA_URL, default http://ollama:11434): nomic-embed-text makes the embeddings, llama3.2:3b writes the
answers, both at temperature 0 with a fixed seed so a rerun prints the same thing.
"""
import json
import math
import os
import sys
import time
import urllib.request
from pathlib import Path

URL = os.environ.get("OLLAMA_URL", "http://ollama:11434")
EMBED = os.environ.get("EMBED_MODEL", "nomic-embed-text")
CHAT = os.environ.get("CHAT_MODEL", "llama3.2:3b")
DOCS = Path(os.environ.get("DOCS", "docs"))
INDEX = Path(os.environ.get("INDEX", "index.json"))
TOP = 3
WIDTH = int(os.environ.get("WIDTH", "44"))  # short lines: the help desk window is narrow
OPTS = {"temperature": 0, "seed": 42}
STORE = "You are the help desk assistant for Kari's Hardware, a small hardware store."


def post(path, body):
    req = urllib.request.Request(URL + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def embed(texts, kind="search_query"):
    # nomic-embed-text is trained with a task prefix: questions and store documents each get their own
    return post("/api/embed", {"model": EMBED, "input": [f"{kind}: {t}" for t in texts]})["embeddings"]


def chat(system, question):
    r = post("/api/chat", {"model": CHAT, "stream": False, "options": OPTS,
                           "messages": [{"role": "system", "content": system}, {"role": "user", "content": question}]})
    return r["message"]["content"].strip()


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def chunks():
    """One chunk per paragraph, each remembering its file."""
    out = []
    for f in sorted(DOCS.glob("*.md")):
        paras = [p.strip() for p in f.read_text().split("\n\n")]
        n = 0
        for p in paras:
            if not p or p.startswith("#"):
                continue
            n += 1
            out.append({"id": f"{f.stem}#{n}", "text": " ".join(p.split())})
    return out


def wrap(text, width=WIDTH, indent="   "):
    words, lines, line = text.split(), [], ""
    for w in words:
        if line and len(line) + 1 + len(w) > width - len(indent):
            lines.append(indent + line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        lines.append(indent + line)
    return "\n".join(lines)


def cmd_ask(q):
    print(wrap(chat(STORE, q), indent=""))


def cmd_chunk(only=None):
    cs = chunks()
    files = sorted({c["id"].split("#")[0] for c in cs})
    shown = [c for c in cs if not only or c["id"].startswith(only)]
    for c in shown:
        t = c["text"]
        print(f"{c['id']:<11} {t[:28] + '...' if len(t) > 31 else t}")
    print(f"{len(cs)} chunks from {len(files)} files")


def cmd_embed(text):
    v = embed([text])[0]
    print(f"{len(v)} numbers: [" + ", ".join(f"{x:.3f}" for x in v[:4]) + ", ...]")


def cmd_similar(a, b):
    va, vb = embed([a, b])
    print(f"{cosine(va, vb):.2f}  {a!r}\n      vs {b!r}")


def cmd_index():
    t = time.time()
    cs = chunks()
    vs = embed([c["text"] for c in cs], "search_document")
    for c, v in zip(cs, vs):
        c["vector"] = v
    INDEX.write_text(json.dumps(cs))
    print(f"Embedded {len(cs)} chunks, {len(vs[0])} numbers each")
    print(f"in {time.time() - t:.1f} s -> {INDEX}")


def search(q):
    if not INDEX.exists():
        raise SystemExit("no index.json yet: run index first")
    cs = json.loads(INDEX.read_text())
    qv = embed([q])[0]
    scored = sorted(((cosine(qv, c["vector"]), c) for c in cs), key=lambda s: -s[0])
    return scored[:TOP]


def cmd_search(q):
    for s, c in search(q):
        t = c["text"]
        print(f"{s:.2f}  {c['id']:<10} {t[:22] + '...' if len(t) > 25 else t}")


def prompt_for(q, hits):
    context = "\n\n".join(f"[{c['id']}] {c['text']}" for _, c in hits)
    system = (f"{STORE} Answer the customer's question using only the store documents below. "
              "If the documents do not contain the answer, say: I don't know, please ask at the counter. "
              "If you answer, end with the document id you used in square brackets.\n\nStore documents:\n" + context)
    return system


def cmd_rag(q, show=False):
    hits = search(q)
    system = prompt_for(q, hits)
    if show:
        print("Top 3: " + ", ".join(c["id"] for s, c in hits))
        print(f"Prompt: {len(system.split()) + len(q.split())} words (3 chunks + question)")
        print("Answer:")
    print(wrap(chat(system, q), indent=""))


def main():
    name = Path(sys.argv[0]).name.replace(".py", "")
    args = sys.argv[1:]
    if name == "helpdesk":
        name, args = args[0], args[1:]
    show = "--show" in args
    args = [a for a in args if a != "--show"]
    {"ask": lambda: cmd_ask(" ".join(args)),
     "chunk": lambda: cmd_chunk(args[0] if args else None),
     "embed": lambda: cmd_embed(" ".join(args)),
     "similar": lambda: cmd_similar(args[0], args[1]),
     "index": cmd_index,
     "search": lambda: cmd_search(" ".join(args)),
     "rag": lambda: cmd_rag(" ".join(args), show)}[name]()


if __name__ == "__main__":
    main()
