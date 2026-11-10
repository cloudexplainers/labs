# The weather station's small Linux box for P102 "Linux Bash Scripting: Full Tutorial for Beginners": a stock
# Ubuntu 24.04 with its own bash, plus ShellCheck from Ubuntu's archive. Ana's home folder holds one CSV file
# per sensor (made-up readings, one line per hour). The scripts she writes wait in /srv/steps and are copied into
# her home folder off camera, one step at a time, without the execute permission, like a file saved from an editor.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends shellcheck procps \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana
COPY --chown=ana:ana home /home/ana
RUN mkdir /home/ana/backups && chown ana:ana /home/ana/backups /home/ana
COPY --chown=ana:ana s1 /srv/steps/s1
COPY --chown=ana:ana s3 /srv/steps/s3
COPY --chown=ana:ana s3b /srv/steps/s3b
COPY --chown=ana:ana s4 /srv/steps/s4
COPY --chown=ana:ana s5 /srv/steps/s5
COPY --chown=ana:ana s5b /srv/steps/s5b
COPY --chown=ana:ana s6 /srv/steps/s6
COPY --chown=ana:ana s8a /srv/steps/s8a
COPY --chown=ana:ana s8b /srv/steps/s8b
COPY --chown=ana:ana s8c /srv/steps/s8c
COPY --chown=ana:ana s8d /srv/steps/s8d
COPY --chown=ana:ana s9 /srv/steps/s9
COPY --chown=ana:ana s10 /srv/steps/s10
CMD ["sleep", "infinity"]
