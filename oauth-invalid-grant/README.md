# How to Fix OAuth 'invalid_grant' Errors

Video: https://youtu.be/gMIN9AkkcIQ  
Written version: https://cloudexplainers.com/how-to-fix-oauth-invalid-grant-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile.id`](lab/Dockerfile.id)
- [`lab/Dockerfile.server`](lab/Dockerfile.server)
- [`lab/exchange`](lab/exchange)
- [`lab/refresh`](lab/refresh)
- [`lab/shuttle-realm.json`](lab/shuttle-realm.json)
- [`lab/signin`](lab/signin)
- [`lab/signout`](lab/signout)

## Commands, in the order the video runs them

### Not a wrong secret

```sh
# john@server:~$
SECRET=not-the-secret exchange
signin
exchange
```

### A code used twice

```sh
# john@server:~$
exchange
exchange
refresh
```

### A code too old

```sh
# john@server:~$
signin
sleep 61; exchange
```

### A different redirect address

```sh
# john@server:~$
REDIRECT_URI=https://shuttle.test/callback/ exchange
exchange
```

### A verifier from another sign-in

```sh
# john@server:~$
signin
CODE=$(cat ~/flow/first) exchange
VERIFIER= exchange
```

### A code for another app

```sh
# john@server:~$
signin
CLIENT=dispatch-desk SECRET=$(cat ~/.desk-secret) exchange
```

### Refresh tokens: signed out or reused

```sh
# john@server:~$
refresh
signout
refresh
refresh
TOKEN=$(cat ~/flow/old) refresh
refresh
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
