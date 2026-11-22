# Dave's laptop for P151 "Golang Error Return Values in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install
# steps say). Dave's project is ~/cart (go mod init cart, done at build); the versions of main.go he types in his
# editor wait in /srv/steps and are copied in off camera, then shown with sed.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash dave \
 && touch /home/dave/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/dave/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=dave:dave steps /srv/steps
USER dave
RUN mkdir -p /home/dave/cart && cd /home/dave/cart && /usr/local/go/bin/go mod init cart 2>/dev/null \
 && cp /srv/steps/ignore/main.go . && /usr/local/go/bin/go build -o /dev/null .
USER root
CMD ["sleep", "infinity"]
