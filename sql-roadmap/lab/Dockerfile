# P075's lab: Linda's laptop. She keeps her book club's lending records in PostgreSQL. A stock Ubuntu 24.04 with
# Ubuntu's own PostgreSQL 16 and psql, and Ubuntu's python3-psycopg2 for the small sign-up script in stage 8.
# Linda is an ordinary user; the database "club" is hers (role linda, not a superuser).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends postgresql python3 python3-psycopg2 \
      less locales >/dev/null && rm -rf /var/lib/apt/lists/* \
 && userdel -r ubuntu && useradd -m -s /bin/bash linda && touch /home/linda/.hushlogin
COPY start.sh /start.sh
CMD ["/start.sh"]
