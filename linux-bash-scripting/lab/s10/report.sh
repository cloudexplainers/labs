#!/bin/bash
# report.sh: tonight's station report, then a backup
set -euo pipefail

dir=${1:-readings}
dest="$HOME/backups"
today=$(date +%F)

highest() {
  sort -t, -k2 -n "$1" | tail -n 1 | cut -d, -f2
}

rows=""
for file in "$dir"/*.csv; do
  name=$(basename "$file" .csv)
  count=$(wc -l < "$file")
  top=$(highest "$file")
  if (( count < 24 )); then
    status="missing"
  else
    status="ok"
  fi
  echo "$name: $count readings, highest $top C, $status"
  rows+="<tr><td>$name</td><td>$count of 24</td>"
  rows+="<td>$top C</td><td class=\"$status\">$status</td></tr>"
done

cat > report.html <<EOF
<link rel="stylesheet" href="style.css">
<title>Station report</title>
<h1>Station report</h1>
<p class="sub">$today, written by report.sh</p>
<table>
<tr><th>Sensor</th><th>Readings</th><th>Highest</th><th>Status</th></tr>
$rows
</table>
EOF

mkdir -p "$dest"
tar -czf "$dest/readings-$today.tar.gz" "$dir"
echo "Backup saved: $dest/readings-$today.tar.gz"
