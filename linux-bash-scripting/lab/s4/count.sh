#!/bin/bash
# count.sh: how many readings did a sensor send?
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 SENSOR" >&2
  exit 1
fi
sensor=$1
file="readings/$sensor.csv"
if [[ ! -f "$file" ]]; then
  echo "No readings for $sensor" >&2
  exit 2
fi
count=$(wc -l < "$file")
echo "$sensor: $count readings"
if (( count < 24 )); then
  echo "WARNING: $((24 - count)) missing" >&2
fi
