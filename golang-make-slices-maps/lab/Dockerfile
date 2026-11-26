# Trish's laptop for P157 "Golang make() for Slices and Maps in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install
# steps say). Trish's project is ~/harvest (go mod init harvest, done at build), her apple orchard's harvest
# counts; each version of the Go files she types in her editor waits in /srv/steps and is copied in off camera.
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
RUN mkdir -p /home/trish/harvest && cd /home/trish/harvest && /usr/local/go/bin/go mod init harvest 2>/dev/null \
 && for s in /srv/steps/*/; do rm -f *.go; cp $s/*.go . && /usr/local/go/bin/go vet . || exit 1; done \
 && rm -f *.go
USER root
CMD ["sleep", "infinity"]
