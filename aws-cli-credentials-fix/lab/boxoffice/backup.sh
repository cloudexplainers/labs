#!/bin/bash
# Riverside Theatre: copy tonight's box-office sales to the backup bucket.
aws s3 cp /srv/boxoffice/sales.csv s3://riverside-box-office/sales/sales-$(date +%F).csv
