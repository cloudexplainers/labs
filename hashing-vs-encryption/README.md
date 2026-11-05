# Hashing vs Encryption in Cybersecurity: When Each One Wins

Video: https://youtu.be/CblJN9y8Ldg  
Written version: https://cloudexplainers.com/hashing-vs-encryption-in-cybersecurity-when-each-one-wins/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/old_shop.py`](lab/old_shop.py)
- [`lab/shop.py`](lab/shop.py)
- [`lab/speed.py`](lab/speed.py)

## Commands, in the order the video runs them

### Hashing, for real

```sh
# ana@shop:~$
echo -n hello | sha256sum
echo -n Hello | sha256sum
ls -lh /usr/bin/bash
sha256sum /usr/bin/bash
```

### Encryption, for real

```sh
# ana@shop:~$
cat address.txt
openssl rand -base64 32 > shop.key
openssl enc -aes-256-cbc -pbkdf2 -a -pass file:shop.key -in address.txt
openssl enc -aes-256-cbc -pbkdf2 -a -pass file:shop.key -in address.txt -out address.enc
cat address.enc
openssl enc -d -aes-256-cbc -pbkdf2 -a -pass file:shop.key -in address.enc
openssl rand -base64 32 > wrong.key
openssl enc -d -aes-256-cbc -pbkdf2 -a -pass file:wrong.key -in address.enc -out /dev/null
```

### Passwords: hashing wins

```sh
# ana@shop:~$
python3 old_shop.py signup ben sunshine1
python3 old_shop.py signup cara sunshine1
cat old_accounts.txt
```

### Good password hashing

```sh
# ana@shop:~$
python3 shop.py signup ben sunshine1
python3 shop.py signup cara sunshine1
cat accounts.txt
python3 shop.py login ben sunshine1
python3 shop.py login ben sunshine2
```

### Downloads: hashing again

```sh
# ana@shop:~$
sha256sum shop-app.tar.gz > shop-app.sha256
cat shop-app.sha256
sha256sum -c shop-app.sha256
echo x >> shop-app.tar.gz
sha256sum -c shop-app.sha256
```

### Look-alikes

```sh
# ana@shop:~$
echo -n '12 Elm Street' | base64
echo MTIgRWxtIFN0cmVldA== | base64 -d; echo
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
