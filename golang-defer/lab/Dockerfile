# Rich's laptop for P158 "Golang defer Statements in 5 Minutes": a stock Ubuntu 24.04 with Go copied in from the
# official golang image (the same files as the go.dev download, unpacked into /usr/local/go, as go.dev's install
# steps say). Rich runs the watering box of a community vegetable patch; his project is ~/patch (go mod init patch,
# done at build) with one watering log per bed per day in ~/patch/readings (2,000 small files, made at build). Each
# version of the Go files he types in his editor waits in /srv/steps and is copied in off camera.
FROM golang:1.27 AS go
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash rich \
 && touch /home/rich/.hushlogin \
 && echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/rich/.bashrc
COPY --from=go /usr/local/go /usr/local/go
COPY --chown=rich:rich steps /srv/steps
USER rich
RUN mkdir -p /home/rich/patch/readings && cd /home/rich/patch && /usr/local/go/bin/go mod init patch 2>/dev/null \
 && for i in $(seq 1 2000); do n=$(printf %04d $i); printf '%s\n%s\n' $(( i % 7 + 3 )) $(( i % 5 + 2 )) > readings/day-$n.log; done \
 && for s in /srv/steps/*/; do rm -f *.go; cp $s/*.go . && /usr/local/go/bin/go vet . || exit 1; done \
 && rm -f *.go
USER root
CMD ["sleep", "infinity"]
