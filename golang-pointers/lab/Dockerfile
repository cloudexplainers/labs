# Trish's laptop for P150 "Golang Pointers in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the official
# golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install steps say).
# Trish's project is ~/walks (go mod init walks, done at build); the versions of main.go she types in her editor wait
# in /srv/steps and are copied in off camera, then shown with cat.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash trish \
 && touch /home/trish/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/trish/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=trish:trish steps /srv/steps
USER trish
RUN mkdir -p /home/trish/walks && cd /home/trish/walks && /usr/local/go/bin/go mod init walks 2>/dev/null \
 && cp /srv/steps/copy/main.go . && /usr/local/go/bin/go build -o /dev/null . 
USER root
CMD ["sleep", "infinity"]
