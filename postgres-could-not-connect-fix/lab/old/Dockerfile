# P142's older laptop: Ubuntu 20.04 with its own psql 12, whose libpq still words the error the old way
# ("could not connect to server: Connection refused"). No systemd: it only runs psql.
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client sudo \
 && useradd -m -s /bin/bash ana && touch /home/ana/.hushlogin
CMD ["sleep", "infinity"]
