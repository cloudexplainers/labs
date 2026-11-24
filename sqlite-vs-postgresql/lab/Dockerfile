# P107 lab: a small real estate office. One stock Ubuntu 24.04 image, two targets:
#   office   the office server that runs the listings site: Ubuntu's sqlite3 3.45 and PostgreSQL 16, Python 3.12 with
#            its built-in sqlite3 module and Ubuntu's psycopg2; user joe
#   pc       Jess's PC: Ubuntu's sqlite3 and psql (client only); user jess
FROM ubuntu:24.04 AS base
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      sqlite3 postgresql-client python3 procps iproute2 less >/dev/null && rm -rf /var/lib/apt/lists/*

FROM base AS pc
RUN useradd -m -s /bin/bash jess
COPY --chown=jess:jess pgpass /home/jess/.pgpass
RUN chmod 600 /home/jess/.pgpass
CMD ["sleep", "infinity"]

FROM base AS office
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      postgresql python3-psycopg2 >/dev/null && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash joe
RUN echo "listen_addresses = '*'" >> /etc/postgresql/16/main/postgresql.conf \
 && echo "host listings jess 0.0.0.0/0 scram-sha-256" >> /etc/postgresql/16/main/pg_hba.conf
COPY --chown=joe:joe site/ /home/joe/site/
COPY start.sh /start.sh
CMD ["/start.sh"]
