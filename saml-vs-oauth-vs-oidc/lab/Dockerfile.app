# The three small services of the lab: Payroll (SAML), Remindly (OAuth 2.0 + OpenID Connect) and the calendar API.
FROM python:3.12-slim
RUN pip install --no-cache-dir "pyjwt[crypto]==2.10.1" requests==2.32.5 signxml lxml \
 && apt-get update -qq && apt-get install -y -qq jq curl >/dev/null && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash dev && mkdir -p /srv/log /srv/data && chown dev /srv/log /srv/data \
 && for f in oauth_tokens.json oidc_tokens.json id_token.json; do ln -s /srv/data/$f /home/dev/$f; done
COPY common.py samlcheck.py payroll.py remindly.py calendar_api.py /srv/
COPY saml-show saml-check calendar-api /usr/local/bin/
WORKDIR /srv
