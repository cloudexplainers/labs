# P131's lab images, one Dockerfile with three targets (portal, proxy, pc).
FROM python:3.12-slim AS certs
RUN pip install -q cryptography
COPY make_certs.py /
RUN python /make_certs.py /certs

# The co-op's milk portal: stock nginx with the certificates above.
FROM nginx:stable AS portal
COPY --from=certs /certs/portal.crt /certs/portal.key /certs/tank.crt /certs/tank.key /etc/nginx/certs/
COPY portal/nginx.conf /etc/nginx/conf.d/default.conf

# The co-op office network's TLS inspection proxy: stock mitmproxy with the office's own inspection CA.
FROM mitmproxy/mitmproxy:12.3.1 AS proxy
COPY --from=certs /certs/office-proxy.pem /home/mitmproxy/.mitmproxy/mitmproxy-ca.pem
CMD ["mitmdump", "--listen-port", "8080", "--set", "confdir=/home/mitmproxy/.mitmproxy", "-q"]

# Chris's farm PC and Sarah's laptop at the co-op office: a stock Ubuntu 24.04 image with Ubuntu's own Python 3.12,
# venv, curl and sudo. Chris may use sudo without a password (a lab shortcut, said in the brief). The co-op's CA
# file sits in ~/Downloads, as the co-op emailed it; the office proxy's CA sits in Sarah's ~/Downloads.
FROM ubuntu:24.04 AS pc
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv python3-pip-whl sudo ca-certificates curl less \
 && userdel -r ubuntu \
 && for u in chris sarah; do useradd -m -s /bin/bash $u; touch /home/$u/.hushlogin; mkdir /home/$u/Downloads; done \
 && echo 'chris ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/chris \
 && echo 'sarah ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/sarah
COPY --from=certs --chown=chris:chris /certs/coop-root-ca.crt /home/chris/Downloads/
COPY --from=certs --chown=sarah:sarah /certs/office-proxy-ca.crt /home/sarah/Downloads/
COPY --chown=chris:chris farm /home/chris/milk-tank
COPY --chown=chris:chris steps /home/chris/steps
COPY --chown=sarah:sarah farm /home/sarah/milk-tank
CMD ["sleep", "infinity"]
