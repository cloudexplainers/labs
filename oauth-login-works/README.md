# How OAuth Login Works

Video: https://youtu.be/fRgamIVoEu0  
Written version: https://cloudexplainers.com/how-oauth-login-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.kettle`](lab/Dockerfile.kettle)
- [`lab/Dockerfile.laptop`](lab/Dockerfile.laptop)
- [`lab/Dockerfile.shop`](lab/Dockerfile.shop)
- [`lab/browser`](lab/browser)
- [`lab/kettle-realm.json`](lab/kettle-realm.json)
- [`lab/shop-api`](lab/shop-api)
- [`lab/shop-token`](lab/shop-token)
- [`lab/shop.py`](lab/shop.py)

## Commands, in the order the video runs them

### Sign in with Google

```sh
# ana@laptop:~$
browser signin https://shop.test
```

### The trip through the browser

```sh
# ana@laptop:~$
curl -s -o /dev/null -w '%{redirect_url}\n' https://shop.test/login | tr '?&' '\n\n'
```

### Swapping the code for tokens

```sh
# ana@shop:~$
tail -n 5 /srv/log/shop.log
grep -ci password /srv/log/shop.log
jq '{iss, aud, sub, exp, nonce, name, email}' /srv/data/id_token.json
shop-api me
shop-api me --no-token
```

### Why a stolen code is worthless

```sh
# ana@laptop:~$
KETTLE=https://id.test/realms/kettle/protocol/openid-connect
browser open "$KETTLE/auth?client_id=tea-shop&response_type=code&redirect_uri=https://other-site.test/callback"
# ana@shop:~$
shop-token --again
shop-api me
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
