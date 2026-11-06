# Why Passkeys Can't Be Phished Like Passwords

Video: https://youtu.be/I-8PKe5C9aw  
Written version: https://cloudexplainers.com/why-passkeys-can-t-be-phished-like-passwords/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.laptop`](lab/Dockerfile.laptop)
- [`lab/Dockerfile.site`](lab/Dockerfile.site)
- [`lab/browser`](lab/browser)
- [`lab/site.py`](lab/site.py)

## Commands, in the order the video runs them

### What a password gives away

```sh
# ana@laptop:~$
curl -s -d user=ana -d password=tea-for-two https://shop.test/login
curl -s -d user=ana -d password=tea-for-tree https://shop.test/login
# ana@shop:~$
tail -n 1 /srv/log/site.log
```

### What a passkey is

```sh
# ana@laptop:~$
browser passkeys
browser signup https://shop.test
browser passkeys
# ana@shop:~$
tail -n 1 /srv/log/site.log
jq .ana /srv/data/users.json
tail -n 1 /srv/log/site.log
# ana@laptop:~$
browser signin https://shop.test --show-signed
```

### Why the fake page gets nothing

```sh
# ana@laptop:~$
browser signin https://other-site.test --ask-for shop.test
browser signin https://other-site.test
# ana@shop:~$
tail -n 2 /srv/log/site.log
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
