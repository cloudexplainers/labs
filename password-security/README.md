# Password Security: Why Hackers Crack Weak Passwords

Video: https://youtu.be/Fi6mMsU6Now  
Written version: https://cloudexplainers.com/password-security-why-hackers-crack-weak-passwords/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/pwned.py`](lab/pwned.py)
- [`lab/space.py`](lab/space.py)

## Commands, in the order the video runs them

### How cracking works

```sh
# ana@shop:~$
python3 space.py
```

### Guess lists come first

```sh
# ana@shop:~$
python3 pwned.py sunshine1
python3 pwned.py 'Sunshine1!'
python3 pwned.py 'P@ssw0rd'
```

### What protects you

```sh
# ana@shop:~$
wc -l words.txt
shuf -n 5 words.txt | paste -sd-
python3 pwned.py moneybags-quill-growing-clunky-poem
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
