# P125's dispatch board PC, "board": a stock Ubuntu 24.04 with Ubuntu's MySQL client and Python with PyMySQL (and the cryptography package it needs for
# MySQL 8's default sign-in method). The
# board program (~/board/board.py) reads its connection settings from ~/board/board.ini and shows today's jobs from
# the office server's dispatch database. Trish has a login here.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends mysql-client python3 python3-pymysql python3-cryptography \
      iproute2 procps less nano ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash trish \
 && touch /home/trish/.hushlogin
COPY --chown=trish:trish board /home/trish/board
CMD ["sleep", "infinity"]
