# MCP Servers: Full Tutorial for Beginners

Video: https://youtu.be/GLjcyl-hN6Q  
Written version: https://cloudexplainers.com/mcp-servers-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/call.jsonl`](lab/call.jsonl)
- [`lab/car-lot/ask`](lab/car-lot/ask)
- [`lab/car-lot/cars.csv`](lab/car-lot/cars.csv)
- [`lab/car-lot/show_calls.py`](lab/car-lot/show_calls.py)
- [`lab/hello.jsonl`](lab/hello.jsonl)
- [`lab/steps/broken/server.py`](lab/steps/broken/server.py)
- [`lab/steps/first/server.py`](lab/steps/first/server.py)
- [`lab/steps/full/server.py`](lab/steps/full/server.py)
- [`lab/steps/old/server.py`](lab/steps/old/server.py)
- [`lab/steps/sold/server.py`](lab/steps/sold/server.py)
- [`lab/steps/toolerror/server.py`](lab/steps/toolerror/server.py)
- [`lab/steps/web_all/web.py`](lab/steps/web_all/web.py)
- [`lab/steps/web_local/web.py`](lab/steps/web_local/web.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### A car lot's own AI helper

```sh
# linda@laptop:~/car-lot$
./ask "A customer wants a blue hatchback under 9000 dollars. What do we have? Answer in two sentences."
```

### Setting up with uv

```sh
# linda@office:~$
uv --version
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv --version
uv init --bare car-lot
cd car-lot
# linda@office:~/car-lot$
uv add "mcp[cli]"
cat pyproject.toml
cat cars.csv
```

### Your first tool

```sh
# linda@office:~/car-lot$
head -6 server.py
uv run server.py
cat server.py
uv run server.py
^D
```

### What travels over the wire

```sh
# linda@office:~/car-lot$
cat hello.jsonl
(cat hello.jsonl; sleep 1) | uv run server.py | jq
tail -1 call.jsonl
(cat call.jsonl; sleep 1) | uv run server.py | jq
```

### Testing with the MCP Inspector

```sh
# linda@laptop:~/car-lot$
ls
npx @modelcontextprotocol/inspector uv run server.py
```

### Connecting it to Claude Code

```sh
# linda@laptop:~/car-lot$
claude --version
claude mcp add --scope project car-lot -- uv run server.py
cat .mcp.json
cat ask
```

### When the server won't start

```sh
# linda@laptop:~/car-lot$
sed -n '24,27p' server.py
./ask "Is the Honda Fit, A12, still for sale? One sentence."
uv run server.py
sed -n '24,27p' server.py
```

### Tools that change things

```sh
# linda@laptop:~/car-lot$
./ask "Mark A12 as sold. One sentence."
./ask --allow mark_sold "Mark A12 as sold. One sentence."
grep A12 cars.csv
```

### Errors the model can read

```sh
# linda@laptop:~/car-lot$
./ask --allow mark_sold "Mark Z99 as sold. One sentence."
sed -n '5p;37p' server.py
./ask --allow mark_sold "Mark Z99 as sold. One sentence."
```

### Resources and prompts

```sh
# linda@laptop:~/car-lot$
sed -n '40,57p' server.py
./ask "/mcp__car-lot__write_listing D21"
```

### Serving it over the network

```sh
# linda@office:~/car-lot$
diff server.py web.py
uv run web.py
# rob@sales-desk:~$
npx @modelcontextprotocol/inspector --cli http://office:8000/mcp --transport http --method tools/list
# linda@office:~/car-lot$
diff server.py web.py
uv run web.py
# rob@sales-desk:~$
npx @modelcontextprotocol/inspector --cli http://office:8000/mcp --transport http --method tools/list | jq -r '.tools[].name'
```

### Keeping it safe

```sh
# rob@sales-desk:~$
npx @modelcontextprotocol/inspector --cli http://office:8000/mcp --transport http --method tools/call --tool-name mark_sold --tool-arg stock=B07
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
