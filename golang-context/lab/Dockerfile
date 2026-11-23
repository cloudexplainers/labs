# John's laptop for P154 "Golang context.Context in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install
# steps say), curl from Ubuntu. John's project is ~/garden (go mod init garden, done at build), the garden center's
# small stock-check server; each version of main.go he types in his editor waits in /srv/steps and is copied in off
# camera. The supplier (lab/supplier, every answer takes 8 s) is built here and runs as the container's main process.
FROM golang:1.27 AS go
COPY supplier /src/supplier
RUN cd /src/supplier && go mod init supplier 2>/dev/null && go build -o /supplier .
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps curl \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash john \
 && touch /home/john/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/john/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --from=go /supplier /usr/local/bin/supplier
COPY --chown=john:john steps /srv/steps
USER john
RUN mkdir -p /home/john/garden && cd /home/john/garden && /usr/local/go/bin/go mod init garden 2>/dev/null \
 && for s in /srv/steps/*/; do cp $s/main.go . && /usr/local/go/bin/go build -o /dev/null . || exit 1; done \
 && rm main.go
USER root
CMD ["supplier"]
