# How Authenticator App Login Codes Work (TOTP)

Video: https://youtu.be/xo93ciOl-Pc  
Written version: https://cloudexplainers.com/how-authenticator-app-login-codes-work-totp/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/authenticator`](lab/authenticator)
- [`lab/diveshop.py`](lab/diveshop.py)
- [`lab/diveshop.service`](lab/diveshop.service)
- [`lab/totp-steps`](lab/totp-steps)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### No signal, still a code

```sh
# ana@phone:~$
ping -c 1 -W 2 1.1.1.1
authenticator
# ana@laptop:~$
curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=188299
```

### The QR code is the secret

```sh
# ana@phone:~$
authenticator scan qr.png
zbarimg -q --raw qr.png
```

### Thirty-second steps

```sh
# ana@phone:~$
date +%s; echo $(( $(date +%s) / 30 ))
# ana@shop:~$
date +%s; echo $(( $(date +%s) / 30 ))
```

### From secret to six digits

```sh
# ana@shop:~$
sudo totp-steps ana
# ana@phone:~$
authenticator
```

### What the shop keeps

```sh
# ana@shop:~$
sudo jq -r '.ana.password[:40], .ana.totp_secret' /var/lib/diveshop/users.json
```

### How old can a code be?

```sh
# ana@phone:~$
authenticator
# ana@laptop:~$
date +%T; curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=878306
# ana@shop:~$
journalctl -u diveshop -o cat -n 1
# ana@phone:~$
authenticator
# ana@laptop:~$
date +%T; curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=778132
```

### One code, one login

```sh
# ana@phone:~$
authenticator
# ana@laptop:~$
curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=475814
curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=475814
```

### A phone with the wrong time

```sh
# ana@phone:~$
authenticator
# ana@laptop:~$
date +%T; curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=073930
curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=020773
```

### Guessing six digits

```sh
# ana@laptop:~$
for c in 111111 222222 333333 444444 555555 666666; do curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=$c; done
curl -s shop/login -d user=ana -d password=coral-reef-9 -d code=741739
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
