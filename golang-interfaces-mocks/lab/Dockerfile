# Tom's laptop for P159 "Golang Interfaces and Mocks in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install steps
# say). Tom runs a roadside egg stand with a card reader; his project is ~/eggs (go mod init eggstand, done at build).
# cardsvc stands in for the payment company's card service on 127.0.0.1:9000 (about a second per charge); it is
# started and stopped off camera. Each version of the Go files Tom types in his editor waits in /srv/steps and is
# copied in off camera.
FROM golang:1.27 AS go
COPY cardsvc /src/cardsvc
RUN cd /src/cardsvc && go mod init cardsvc 2>/dev/null && CGO_ENABLED=0 go build -o /cardsvc .
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash tom \
 && touch /home/tom/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/tom/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --from=go /cardsvc /usr/local/bin/cardsvc
COPY --chown=tom:tom steps /srv/steps
USER tom
RUN mkdir -p /home/tom/eggs && cd /home/tom/eggs && /usr/local/go/bin/go mod init eggstand 2>/dev/null \
 && for s in real iface mock; do rm -f *.go; cp /srv/steps/$s/*.go . && /usr/local/go/bin/go vet . || exit 1; done \
 && /usr/local/go/bin/go test -c -o /dev/null . && rm -f *.go
USER root
CMD ["sleep", "infinity"]
