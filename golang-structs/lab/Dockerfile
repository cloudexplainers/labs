# Sue's laptop for P155 "Golang Structs in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the official
# golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install steps say).
# Sue's project is ~/arcade (go mod init arcade, done at build), the high score board of a retro gaming arcade; each
# version of main.go she types in her editor waits in /srv/steps and is copied in off camera. Every version builds
# here except "added", which is the one that fails on camera.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash sue \
 && touch /home/sue/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/sue/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=sue:sue steps /srv/steps
USER sue
RUN mkdir -p /home/sue/arcade && cd /home/sue/arcade && /usr/local/go/bin/go mod init arcade 2>/dev/null \
 && for s in /srv/steps/*/; do [ "$(basename $s)" = added ] && continue; cp $s/main.go . && /usr/local/go/bin/go build -o /dev/null . || exit 1; done \
 && rm main.go
USER root
CMD ["sleep", "infinity"]
