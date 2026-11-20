# P073's laptop: a stock Ubuntu 24.04 image with Ubuntu's own Python 3.12 and its venv module (python3-venv), plus
# python3-yaml from apt (a package the system Python has and a new virtual environment doesn't see), tree and time.
# Ana is the only user; packages from PyPI are installed on camera (numpy 1.26.4 and the latest numpy 2).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv python3-yaml tree time \
      ca-certificates less procps \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana \
 && touch /home/ana/.hushlogin
COPY --chown=ana:ana hive-log /home/ana/hive-log
COPY --chown=ana:ana honey-chart /home/ana/honey-chart
CMD ["sleep", "infinity"]
