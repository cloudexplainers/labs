#!/bin/bash
# Card reader test: N payments, spread over the 12 washers, as the machines would send them.
n=${1:-100}; ok=0
for i in $(seq "$n"); do
  m=$(printf 'washer-%02d' $(( (i - 1) % 12 + 1 )))
  code=$(curl -s -m 5 -o /dev/null -w '%{http_code}' -X POST "http://localhost:8000/pay/$m")
  if [ "$code" = 200 ]; then ok=$((ok + 1)); else echo "payment $i ($m): failed, HTTP $code"; break; fi
done
echo "$ok of $n payments went through"
