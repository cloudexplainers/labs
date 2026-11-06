# How to Fix Claude Code Billing Your API Key Instead of Your Plan

Video: https://youtu.be/UtNMBfxjTTs  
Written version: https://cloudexplainers.com/how-to-fix-claude-code-billing-your-api-key-instead-of-your-plan/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/app.py`](lab/app.py)

## Commands, in the order the video runs them

### Billed for the wrong thing

```sh
claude -p "Write a one-line welcome for Ana's tea shop"
```

### The usual fix

```sh
env | grep ANTHROPIC
unset ANTHROPIC_API_KEY
claude auth status | grep -E 'authMethod|apiKeySource'
claude -p "Write a one-line welcome for Ana's tea shop"
```

### Why Claude Code picks the key

```sh
claude auth status | grep -E 'authMethod|apiKeySource'
```

### The Yes you said once

```sh
claude
```

### The No that scripts ignore

```sh
claude -p "Write a one-line welcome for Ana's tea shop"
```

### Keep the key for your own code

```sh
ANTHROPIC_API_KEY=$(cat shop-key.txt) python3 app.py
claude auth status | grep -E 'authMethod|apiKeySource'
python3 app.py
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
