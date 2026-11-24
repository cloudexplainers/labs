# Joe's laptop for P156 "Golang for range Loops in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install
# steps say). Joe's project is ~/catchlog (go mod init catchlog, done at build), the catch log of his fishing
# charter boat; each version of main.go he types in his editor waits in /srv/steps and is copied in off camera.
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
RUN mkdir -p /home/joe/catchlog && cd /home/joe/catchlog && /usr/local/go/bin/go mod init catchlog 2>/dev/null \
 && for s in /srv/steps/*/; do cp $s/main.go . && /usr/local/go/bin/go build -o /dev/null . || exit 1; done \
 && rm main.go
USER root
CMD ["sleep", "infinity"]
