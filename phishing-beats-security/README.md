# Why Phishing Beats Good Security (and How to Spot It)

Video: https://youtu.be/qXoc9G2eICo  
Written version: https://cloudexplainers.com/why-phishing-beats-good-security-and-how-to-spot-it/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/code_check.py`](lab/code_check.py)
- [`lab/passkey_demo.py`](lab/passkey_demo.py)
- [`lab/sender_check.py`](lab/sender_check.py)
- [`lab/url_check.py`](lab/url_check.py)

## Commands, in the order the video runs them

### Why good security doesn't help

```sh
# ana@laptop:~/lab$
python3 code_check.py
```

### Spot it: the address

```sh
# ana@laptop:~/lab$
python3 url_check.py https://bank.example/login
python3 url_check.py https://bank.example.account-check.test/login
python3 url_check.py https://bank.example@account-check.test/login
python3 url_check.py https://bank-example.test/login
python3 url_check.py https://account-check.test/bank.example/login
```

### Spot it: the sender

```sh
# ana@laptop:~/lab$
python3 sender_check.py 'Bank Security <alerts@bank-example.test>'
python3 sender_check.py 'Bank <alerts@bank.example>'
```

### Stop it without noticing

```sh
# ana@laptop:~/lab$
python3 passkey_demo.py register
python3 passkey_demo.py https://bank.example/login
python3 passkey_demo.py https://bank-example.test/login
python3 passkey_demo.py https://bank-example.test/login --sign-anyway
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
