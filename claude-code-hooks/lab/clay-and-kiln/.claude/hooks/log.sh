#!/bin/bash
# Any event: one line in hooks.log, and the event's input kept in .claude/input/
input=$(cat)
event=$(echo "$input" | jq -r .hook_event_name)
mkdir -p .claude/input && echo "$input" > ".claude/input/$event.json"
echo "$input" | jq -r '[.hook_event_name, .tool_name // "",
  (.tool_input.file_path // .tool_input.command // "" | split("/") | last)] | join(" ")' >> hooks.log
