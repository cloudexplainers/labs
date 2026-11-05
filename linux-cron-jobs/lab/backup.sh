#!/bin/bash
# Back up the shop's orders. Ana runs this every night at 2:30.
set -euo pipefail
cd ~/shop
shop-export > orders.csv
tar -czf ~/backups/orders-$(date +%F-%H%M).tar.gz orders.csv
echo "backup done: $(ls ~/backups | tail -n 1)"
