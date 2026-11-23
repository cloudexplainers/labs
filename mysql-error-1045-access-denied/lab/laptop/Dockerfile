# Mike's laptop for P125: a stock Ubuntu 24.04 with Ubuntu's own docker command and Compose plugin (docker.io,
# docker-compose-v2). The docker command talks to the Mac's Docker engine through its socket, mounted by demo.sh;
# mike is in the socket's group (root) for that only. ~/testdb holds his test copy of the dispatch database: the
# official mysql:8.4 image with a named volume, in compose.yaml.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps docker.io docker-compose-v2 \
      less nano \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash -G root mike \
 && touch /home/mike/.hushlogin
COPY --chown=mike:mike testdb /home/mike/testdb
CMD ["sleep", "infinity"]
