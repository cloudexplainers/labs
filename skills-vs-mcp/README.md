# Agent Skills vs MCP: When Each One Wins

Video: https://youtu.be/8KqTMv8Pmw0  
Written version: https://cloudexplainers.com/agent-skills-vs-mcp-when-each-one-wins/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/agent`](lab/agent)
- [`lab/github.json`](lab/github.json)
- [`lab/mcp.json`](lab/mcp.json)
- [`lab/orders-server/Dockerfile`](lab/orders-server/Dockerfile)
- [`lab/orders-server/server.py`](lab/orders-server/server.py)
- [`lab/requests/call.json`](lab/requests/call.json)
- [`lab/requests/list.json`](lab/requests/list.json)
- [`lab/shop/.claude/skills/late-order-reply/SKILL.md`](lab/shop/.claude/skills/late-order-reply/SKILL.md)

## Commands, in the order the video runs them

### Two problems

```sh
kettle-and-bean$ ./agent "Which of our orders are late right now?"
kettle-and-bean$ ./agent --mcp "Write a reply to the customer of order 1042."
kettle-and-bean$ ls
```

### What an agent sees

```sh
kettle-and-bean$ ./agent "Reply with just: ok"
```

### MCP: access

```sh
kettle-and-bean$ grep -A2 '@mcp.tool' orders-server/server.py
kettle-and-bean$ cat requests/list.json | jq .
kettle-and-bean$ (cat requests/list.json; sleep 1) | docker run -i --rm orders-mcp | jq '.result.tools[] | {name, description}'
kettle-and-bean$ (cat requests/call.json; sleep 1) | docker run -i --rm orders-mcp | jq -c '.result.structuredContent.result[] | {id, customer, days_late}'
kettle-and-bean$ ./agent --mcp "Which of our orders are late right now?"
```

### Skills: know-how

```sh
kettle-and-bean$ find shop -type f
kettle-and-bean$ cat shop/.claude/skills/late-order-reply/SKILL.md
kettle-and-bean$ ./agent --mcp --skill "Write a reply to the customer of order 1042."
kettle-and-bean$ ./agent --mcp --skill "Write a reply to the customer of order 1043."
```

### What each one costs

```sh
kettle-and-bean$ (cat requests/list.json; sleep 2) | docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=demo ghcr.io/github/github-mcp-server stdio 2>/dev/null | jq '.result.tools | length'
kettle-and-bean$ (cat requests/list.json; sleep 2) | docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=demo ghcr.io/github/github-mcp-server stdio 2>/dev/null | jq -c '[.result.tools[] | {name, description, inputSchema}]' | wc -c
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
