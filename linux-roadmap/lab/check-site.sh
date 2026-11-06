#!/bin/bash
# Is Ana's site answering? How full is the disk?
if curl -sf http://localhost > /dev/null; then site=up; else site=DOWN; fi
disk=$(df --output=pcent / | tail -1 | tr -d ' ')
echo "$(date +%H:%M:%S) site $site, disk $disk used"
