#!/bin/bash
# count.sh: how many readings did a sensor send?
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 SENSOR" >&2
  exit 1
fi
sensor=$1
file="readings/$sensor.csv"
count=$(wc -l < "$file")
echo "$sensor: $count readings"
