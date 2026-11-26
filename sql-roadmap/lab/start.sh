#!/bin/sh
# Starts the laptop's PostgreSQL 16 the way Ubuntu's own service does, then stays up.
pg_ctlcluster 16 main start
exec sleep infinity
