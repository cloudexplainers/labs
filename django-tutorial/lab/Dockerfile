# Ana's laptop for P095 "Django Full Tutorial for Beginners": a stock Ubuntu 24.04 with Python 3.12 from apt,
# curl, w3m (a text-mode web browser, so pages can be shown in a terminal) and tree. uv and Django are installed
# on camera, from the internet, like on any laptop. Ana's own files (what she types in her editor) wait in
# /srv/steps and are copied into her project off camera, one step at a time, then shown with cat.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates python3 w3m tree procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana
COPY --chown=ana:ana s1 /srv/steps/s1
COPY --chown=ana:ana s2 /srv/steps/s2
COPY --chown=ana:ana s3 /srv/steps/s3
COPY --chown=ana:ana s4 /srv/steps/s4
COPY --chown=ana:ana s5 /srv/steps/s5
COPY --chown=ana:ana s6 /srv/steps/s6
COPY --chown=ana:ana s7 /srv/steps/s7
CMD ["sleep", "infinity"]
