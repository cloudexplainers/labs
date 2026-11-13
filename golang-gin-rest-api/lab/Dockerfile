# Ana's laptop for P108 "Golang REST API with Gin: Full Tutorial for Beginners": a stock Ubuntu 24.04 with curl,
# jq and tree, and Go copied in from the official golang image (the same files as the go.dev download, unpacked
# into /usr/local/go, as go.dev's install steps say). Gin itself is fetched on camera with go get, from the internet.
# Ana's own files (what she types in her editor) wait in /srv/steps and are copied into her project off camera.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates jq tree procps file git \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana \
 && echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> /home/ana/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=ana:ana steps /srv/steps
CMD ["sleep", "infinity"]
