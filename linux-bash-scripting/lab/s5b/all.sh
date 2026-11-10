#!/bin/bash
# all.sh: check every sensor on the list
while read -r sensor; do
  ./count.sh "$sensor" || echo "  -> check the $sensor sensor"
done < sensors.txt
