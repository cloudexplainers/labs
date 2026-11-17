#!/bin/bash
# Stop: Claude can't finish while the tests fail
input=$(cat)
if [ "$(echo "$input" | jq -r .stop_hook_active)" = "true" ]; then
  exit 0
fi
date +%T >> .claude/tests.log
if ! result=$(python3 -m unittest 2>&1); then
  echo "The tests fail. Fix them before you stop:" >&2
  echo "$result" | grep -E "^(FAIL|AssertionError)" >&2
  exit 2
fi
exit 0
