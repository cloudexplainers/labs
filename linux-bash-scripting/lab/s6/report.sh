#!/bin/bash
# report.sh: one line for every sensor

highest() {
  sort -t, -k2 -n "$1" | tail -n 1 | cut -d, -f2
}

report_line() {
  local file=$1
  local name count
  name=$(basename "$file" .csv)
  count=$(wc -l < "$file")
  echo "$name: $count readings, highest $(highest "$file") C"
}

for file in readings/*.csv; do
  report_line "$file"
done
