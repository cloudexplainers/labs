# AI Agents Will Finally Make Sense After This

Video: https://youtu.be/i9ZaWfUeIGY  
Written version: https://cloudexplainers.com/ai-agents-will-finally-make-sense-after-this/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/agent`](lab/agent)
- [`lab/bill-splitter/split.py`](lab/bill-splitter/split.py)
- [`lab/bill-splitter/test_split.py`](lab/bill-splitter/test_split.py)
- [`lab/raw`](lab/raw)

## Commands, in the order the video runs them

### One sentence in

```sh
agent-lab$ ./agent --session fix "Run the tests (python3 -m unittest), find out why they fail, and fix it."
agent-lab$ ls
agent-lab$ cd bill-splitter
bill-splitter$ cat split.py
bill-splitter$ python3 -m unittest
```

### Chatbot vs agent

```sh
agent-lab$ ./agent --no-tools "Run the tests (python3 -m unittest), find out why they fail, and fix it."
```

### The loop

```sh
agent-lab$ ./raw 1
agent-lab$ cd bill-splitter && python3 -m unittest; cd ..
agent-lab$ grep tip_percent bill-splitter/split.py
```

### Memory

```sh
agent-lab$ ./agent --no-tools "What did we fix in this project last time?"
agent-lab$ ./agent --session fix "Add a one-line note to CLAUDE.md saying what you fixed today."
agent-lab$ cat bill-splitter/CLAUDE.md
agent-lab$ ./agent --no-tools "What did we fix in this project last time?"
```

### Planning

```sh
agent-lab$ ./agent "Install pytest for this project."
```

### Limits

```sh
agent-lab$ ./agent --max-turns 2 "Run the tests (python3 -m unittest), find out why they fail, and fix it."
agent-lab$ grep 'with_tip =' bill-splitter/split.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
