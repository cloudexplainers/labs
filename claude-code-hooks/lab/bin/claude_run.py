"""One headless Claude Code request in the current folder (claude -p, Claude Sonnet, this project's settings only).
Yields the stream-json events. Shared by ask and trial."""
import json
import subprocess

TOOLS = "Read,Edit,Write,Glob,Grep,Bash(python3 *),Bash(python *)"


def events(prompt):
    cmd = ["claude", "-p", prompt, "--model", "sonnet", "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project", "--strict-mcp-config", "--no-session-persistence",
           "--allowedTools", TOOLS]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
    for raw in p.stdout:
        yield json.loads(raw)
    p.wait()
