# How to Fix JWT Token Expired Errors (401 Unauthorized)

Video: https://youtu.be/s83N2fVS1aQ  
Written version: https://cloudexplainers.com/how-to-fix-jwt-token-expired-errors-401-unauthorized/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/api_server.py`](lab/api_server.py)
- [`lab/jwt-extend`](lab/jwt-extend)
- [`lab/login_server.py`](lab/login_server.py)
- [`lab/shop`](lab/shop)

## Commands, in the order the video runs them

### The token that stopped working

```sh
# ana@laptop:~$
date +%T
TOKEN=$(shop token)
curl -si api/orders -H "Authorization: Bearer $TOKEN"
date +%T
curl -si api/orders -H "Authorization: Bearer $TOKEN"
```

### What's inside a JWT

```sh
# ana@laptop:~$
echo $TOKEN | tr . '\n'
echo $TOKEN | cut -d. -f1 | jq -R '@base64d | fromjson'
echo $TOKEN | cut -d. -f2 | jq -R '@base64d | fromjson'
date -d @1793569263 +%T
date +%s
```

### Why tokens expire on purpose

```sh
# ana@laptop:~$
FAKE=$(jwt-extend $TOKEN 3600)
echo $FAKE | cut -d. -f2 | jq -R '@base64d | fromjson'
curl -si api/orders -H "Authorization: Bearer $FAKE"
```

### Fix 1: refresh the token

```sh
# ana@laptop:~$
jq . ~/.shop/tokens.json
shop orders
shop orders
```

### Fix 2: when a new token fails

```sh
# ana@laptop:~$
shop login ana
shop orders
date -u -R; curl -si login/ | grep Date; curl -si api/orders | grep Date
date -u -R; curl -si login/ | grep Date; curl -si api/orders | grep Date
shop orders
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
