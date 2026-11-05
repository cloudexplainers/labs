# Ana's laptop for P070: a stock Ubuntu 24.04 with the sqlite3 command-line tool and Python 3 (its sqlite3 module
# is part of the standard library). No database server is installed.
FROM ubuntu:24.04
RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      sqlite3 python3 file procps >/dev/null && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash ana
COPY --chown=ana:ana shop/ /home/ana/shop/
USER ana
WORKDIR /home/ana/shop
CMD ["sleep", "infinity"]
