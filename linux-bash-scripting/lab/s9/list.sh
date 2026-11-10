#!/bin/bash
# list.sh: count the lines of every file
for f in readings/*.csv; do
  echo "Checking $f"
  wc -l "$f"
done
