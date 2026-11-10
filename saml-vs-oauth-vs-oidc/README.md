# SAML vs OAuth vs OpenID Connect: What's the Difference?

Video: https://youtu.be/cG0xZkPTm74  
Written version: https://cloudexplainers.com/saml-vs-oauth-vs-openid-connect-what-s-the-difference/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.app`](lab/Dockerfile.app)
- [`lab/Dockerfile.laptop`](lab/Dockerfile.laptop)
- [`lab/Dockerfile.maple`](lab/Dockerfile.maple)
- [`lab/browser`](lab/browser)
- [`lab/calendar-api`](lab/calendar-api)
- [`lab/calendar_api.py`](lab/calendar_api.py)
- [`lab/common.py`](lab/common.py)
- [`lab/maple-realm.json`](lab/maple-realm.json)
- [`lab/payroll.py`](lab/payroll.py)
- [`lab/remindly.py`](lab/remindly.py)
- [`lab/saml-check`](lab/saml-check)
- [`lab/saml-show`](lab/saml-show)
- [`lab/samlcheck.py`](lab/samlcheck.py)

## Commands, in the order the video runs them

### Three names, one login?

```sh
# dev@remindly:~$
jq '{token_type, expires_in, scope, id_token}' oauth_tokens.json
```

### SAML: who you are, in XML

```sh
# dev@payroll:~$
saml-show
saml-check
saml-check --change ana@clinic.test dr.lee@clinic.test
```

### OAuth: what an app may do

```sh
# dev@remindly:~$
calendar-api GET /events
calendar-api POST /events
```

### OpenID Connect: one more word

```sh
# dev@remindly:~$
jq '{scope, id_token: .id_token[0:20]}' oidc_tokens.json
jq '{iss, aud, sub, name, email, exp}' id_token.json
calendar-api GET /events --token id
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
