#!/bin/bash
# list.sh: count the lines of every file
for f in $(ls readings); do
  echo "Checking $f"
  wc -l readings/$f
done
