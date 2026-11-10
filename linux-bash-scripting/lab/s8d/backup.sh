#!/bin/bash
# backup.sh: save today's readings in the backup folder
set -euo pipefail
dest="/home/ana/backups"
cd "$dset"
tar -czf "readings-$(date +%F).tar.gz" -C /home/ana readings
echo "Backup done"
