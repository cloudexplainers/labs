# How to Fix a Security Leak: An API Key Pushed to GitHub

Video: https://youtu.be/a0B7pR1FCTU  
Written version: https://cloudexplainers.com/how-to-fix-a-security-leak-an-api-key-pushed-to-github/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/pay_api.py`](lab/pay_api.py)
- [`lab/paylab`](lab/paylab)
- [`lab/payments.py`](lab/payments.py)

## Commands, in the order the video runs them

### The key that didn't go away

```sh
# bot@stranger:~/kettle-shop$
git log --oneline
git show f2971eb:.env
```

### How the key got out

```sh
# ana@laptop:~/kettle-shop$
git status --short
cat .env
git add .
git commit -m "Connect the payment service"
git push
git rm .env
git commit -m "Remove .env"
git push
ls -a
```

### Why deleting it isn't enough

```sh
# bot@stranger:~$
git clone git://git-server/kettle-shop.git
cd kettle-shop
# bot@stranger:~/kettle-shop$
ls -a
gitleaks git -v
KEY=$(git show f2971eb:.env | cut -d= -f2)
curl -s -H "Authorization: Bearer $KEY" payments/v1/customers
```

### Make the key useless

```sh
# ana@laptop:~/kettle-shop$
paylab keys
paylab log key_c58b
paylab roll key_c58b --save .env
paylab keys
# bot@stranger:~/kettle-shop$
curl -s -H "Authorization: Bearer $KEY" payments/v1/customers
# ana@laptop:~/kettle-shop$
git status --short
echo ".env" >> .gitignore
git status --short
git add .gitignore && git commit -m "Keep .env out of Git"
```

### Wipe it from history

```sh
# ana@laptop:~$
git clone git@git-server:kettle-shop.git shop-clean
cd shop-clean
# ana@laptop:~/shop-clean$
git filter-repo --sensitive-data-removal --invert-paths --path .env
git log --oneline
git log --all --oneline -- .env
git push --force --mirror origin
# bot@stranger:~$
git clone git://git-server/kettle-shop.git fresh
cd fresh
# bot@stranger:~/fresh$
gitleaks git -v
cd ~/kettle-shop
# bot@stranger:~/kettle-shop$
git show f2971eb:.env
```

### Stop the next leak

```sh
# ana@laptop:~/shop-clean$
cat .git/hooks/pre-commit
git add settings.py
git commit -m "Quick test"
git log --oneline -1
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
