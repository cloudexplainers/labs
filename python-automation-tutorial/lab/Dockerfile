# Ana's laptop for P092 "Python Automation: Full Tutorial for Beginners": a stock Ubuntu 24.04 with curl, cron and
# sudo. uv, Python packages and Playwright's browser are installed on camera, from the internet, like on any laptop.
# Off-screen helpers that stand in for the outside world (run with the system python3, outside Ana's project):
#   supplier.py  the tea supplier: a JSON stock API that needs a key, and a web portal with a login and no API
#   aiosmtpd     a test mail server on localhost:1025 that prints every message instead of delivering it
#   make_files.py  Ana's messy Downloads folder: daily order exports (CSV) and supplier invoices (PDF)
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates sudo cron python3 \
      python3-aiosmtpd \
 && userdel -r ubuntu \
 && useradd -m -s /bin/bash ana && echo 'ana:tea-for-two' | chpasswd && adduser ana sudo >/dev/null \
 && sed -i 's/^session\s\+required\s\+pam_loginuid.so/#&/' /etc/pam.d/cron \
 && mkdir -p /srv/supplier /srv/mail
COPY supplier.py make_files.py /srv/supplier/
RUN chown ana:ana /srv/mail
