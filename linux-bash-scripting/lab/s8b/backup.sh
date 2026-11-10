#!/bin/bash
# backup.sh: save today's readings in the backup folder
set -e
cd /home/ana/backup
tar -czf "readings-$(date +%F).tar.gz" -C /home/ana readings
echo "Backup done"
