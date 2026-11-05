#!/bin/bash
# Try each "user password" pair from a list against one PostgreSQL server, the way bots on the internet do.
# Lab only: run against our own containers. Usage: guess <host> <list>
host=$1
list=$2
while read -r user pw; do
  PGPASSWORD="$pw" PGCONNECT_TIMEOUT=5 psql -h "$host" -U "$user" -d postgres -Atc 'select 1' >/dev/null 2>/tmp/guess.err
  if [ $? -eq 0 ]; then
    result="LOGGED IN"
  elif grep -q 'password authentication failed' /tmp/guess.err; then
    result="wrong password"
  elif grep -q 'timeout expired' /tmp/guess.err; then
    result="no answer (timed out)"
  elif grep -q 'Connection refused' /tmp/guess.err; then
    result="connection refused"
  else
    result=$(head -1 /tmp/guess.err)
  fi
  printf '%-9s %-9s %s\n' "$user" "$pw" "$result"
done < "$list"
