# Sue's laptop for P140 "How to Fix Golang 'go.mod File Not Found' Errors": a stock Ubuntu 24.04 with Go copied in
# from the official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's
# install steps say) and Ubuntu's own docker command (docker.io, docker-buildx). The docker command talks to the Mac's
# Docker engine through its socket, mounted by demo.sh; sue is in the socket's group (root) for that only.
# Sue's project is ~/departures (no go.mod yet); the files she types in her editor wait in /srv/steps and are copied
# in off camera. Rich has his own login with ~/rail: two modules, board and alerts, cloned before the demo.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps git docker.io docker-buildx \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && for u in sue rich; do useradd -m -s /bin/bash $u && touch /home/$u/.hushlogin \
    && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/$u/.bashrc; done \
 && usermod -aG root sue
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=sue:sue steps /srv/steps
USER sue
RUN mkdir -p /home/sue/departures/tools && cp /srv/steps/board/main.go /home/sue/departures/ \
 && cp /srv/steps/tools/main.go /home/sue/departures/tools/
USER rich
RUN mkdir -p /home/rich/rail/board /home/rich/rail/alerts \
 && cd /home/rich/rail/board && /usr/local/go/bin/go mod init board 2>/dev/null && cp /srv/steps/rail_board/main.go . \
 && cd /home/rich/rail/alerts && /usr/local/go/bin/go mod init alerts 2>/dev/null && cp /srv/steps/alerts/main.go .
USER root
CMD ["sleep", "infinity"]
