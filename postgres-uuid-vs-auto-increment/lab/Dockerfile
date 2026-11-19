# The record store's laptop: PostgreSQL 18's own client tools (psql, pgbench) on Alpine, and Ana's account.
FROM postgres:18-alpine
RUN adduser -D -s /bin/bash ana
COPY pgpass /home/ana/.pgpass
RUN chown ana:ana /home/ana/.pgpass && chmod 600 /home/ana/.pgpass \
 && printf 'export PGUSER=ana PGDATABASE=records\n' > /home/ana/.profile && chown ana:ana /home/ana/.profile
CMD ["sleep", "infinity"]
