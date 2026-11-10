#!/bin/bash
# count.sh: how many readings did a sensor send?
sensor=$1
file="readings/$sensor.csv"
count=$(wc -l < "$file")
echo "$sensor: $count readings"
