# Jim's laptop for P153 "Golang Method Receivers in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install
# steps say). Jim's project is ~/league (go mod init league, done at build), his little league team's season tool;
# the versions of main.go he types in his editor wait in /srv/steps and are copied in off camera. Steps that are
# meant to fail to compile carry a BROKEN file and are skipped by the vet check.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash jim \
 && touch /home/jim/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/jim/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=jim:jim steps /srv/steps
USER jim
RUN mkdir -p /home/jim/league && cd /home/jim/league && /usr/local/go/bin/go mod init league 2>/dev/null \
 && for s in /srv/steps/*/; do [ -e $s/BROKEN ] && continue; cp $s/main.go . && /usr/local/go/bin/go vet . || exit 1; done
USER root
CMD ["sleep", "infinity"]
