# JWT vs Session Cookies: Which One Should You Use?

Video: https://youtu.be/b-nXWVGMwvA  
Written version: https://cloudexplainers.com/jwt-vs-session-cookies-which-one-should-you-use/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.api`](lab/Dockerfile.api)
- [`lab/Dockerfile.laptop`](lab/Dockerfile.laptop)
- [`lab/Dockerfile.store`](lab/Dockerfile.store)
- [`lab/browser`](lab/browser)
- [`lab/shop.py`](lab/shop.py)
- [`lab/show-store`](lab/show-store)

## Commands, in the order the video runs them

### Logged out, still logged in

```sh
# ana@laptop:~$
curl -s -X POST api1.kettle.test/token/logout -H "Authorization: Bearer $TOKEN"
curl -si api1.kettle.test/orders -H "Authorization: Bearer $TOKEN"
```

### What a session is

```sh
# ana@laptop:~$
curl -si -c jar.txt api1.kettle.test/session/login -d user=ana -d password=kettle-2026
curl -si -b jar.txt api1.kettle.test/orders
# root@sessions:~#
show-store
```

### What a JWT carries

```sh
# ana@laptop:~$
TOKEN=$(curl -s api1.kettle.test/token/login -d user=ana -d password=kettle-2026 | jq -r .access_token)
echo $TOKEN
echo $TOKEN | cut -d. -f2 | jq -R '@base64d | fromjson'
```

### A second server

```sh
# ana@laptop:~$
curl -si -b jar.txt api2.kettle.test/orders
curl -si api2.kettle.test/orders -H "Authorization: Bearer $TOKEN"
curl -si api2.kettle.test/token/login -d user=ana -d password=kettle-2026
curl -si -b jar.txt api2.kettle.test/orders
```

### Logging out for real

```sh
# ana@laptop:~$
cp jar.txt old-jar.txt
curl -si -b jar.txt -c jar.txt -X POST api1.kettle.test/session/logout
curl -si -b old-jar.txt api1.kettle.test/orders
# root@sessions:~#
show-store
# ana@laptop:~$
curl -s -X POST api1.kettle.test/token/logout -H "Authorization: Bearer $TOKEN"
curl -si api2.kettle.test/orders -H "Authorization: Bearer $TOKEN"
T2=$(curl -s api1.kettle.test/token/login -d user=ana -d password=kettle-2026 | jq -r .access_token)
curl -si api2.kettle.test/orders -H "Authorization: Bearer $T2"
# root@sessions:~#
show-store
```

### Inside the browser

```sh
# ana@laptop:~$
browser http://api1.kettle.test/
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
