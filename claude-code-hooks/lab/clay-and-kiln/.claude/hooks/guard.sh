#!/bin/bash
# PreToolUse: keep Claude out of .env
input=$(cat)
target=$(echo "$input" | jq -r '.tool_input | .file_path // .command // .path // .pattern // empty')
if [[ "$target" == *.env* ]]; then
  echo "Blocked: .env holds the studio's passwords. Ask Ana." >&2
  exit 2
fi
exit 0
