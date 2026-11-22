# Joe's laptop for P152 "Golang if err != nil Checks in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install
# steps say). Joe's project is ~/flights (go mod init flights, done at build), the flight school's daily schedule
# tool; the versions of main.go he types in his editor wait in /srv/steps and are copied in off camera, then shown
# with sed.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash joe \
 && touch /home/joe/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/joe/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=joe:joe steps /srv/steps
USER joe
RUN mkdir -p /home/joe/flights && cd /home/joe/flights && /usr/local/go/bin/go mod init flights 2>/dev/null \
 && for s in /srv/steps/*/; do cp $s/main.go . && /usr/local/go/bin/go vet . || exit 1; done
USER root
CMD ["sleep", "infinity"]
