# Two-Factor Authentication Will Finally Make Sense

Video: https://youtu.be/UDXk9pui5JQ  
Written version: https://cloudexplainers.com/two-factor-authentication-will-finally-make-sense/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/leak.txt`](lab/leak.txt)

## Commands, in the order the video runs them

### A leaked password

```sh
# thief@thief-pc:~$
cat leak.txt
ssh ana@shop hostname
# ana@shop:~$
sudo journalctl -u ssh -o cat | grep Accepted
```

### Setting up an authenticator

```sh
# ana@shop:~$
google-authenticator -t -d -f -r 3 -R 30 -w 3 -Q NONE
# ana@phone:~$
ls -l shop.key
oathtool --totp -b "$(cat shop.key)"
# ana@shop:~$
google-authenticator -t -d -f -r 3 -R 30 -w 3 -Q NONE
ls -l ~/.google_authenticator
```

### How the code is made

```sh
# ana@phone:~$
ping -c 1 -W 2 shop
date +%s
echo $(( $(date +%s) / 30 ))
oathtool --totp -b "$(cat shop.key)"
# ana@shop:~$
oathtool --totp -b "$(head -1 ~/.google_authenticator)"
# ana@phone:~$
for i in 1 2 3; do date +%T; oathtool --totp -b "$(cat shop.key)"; sleep 30; done
```

### Turning it on

```sh
# ana@shop:~$
sudo sed -i '/@include common-auth/a auth required pam_google_authenticator.so' /etc/pam.d/sshd
grep -n -A1 'common-auth' /etc/pam.d/sshd
printf 'KbdInteractiveAuthentication yes\nAuthenticationMethods keyboard-interactive\n' | sudo tee /etc/ssh/sshd_config.d/00-two-factor.conf
sudo sshd -t && echo config OK
sudo systemctl reload ssh
sudo sshd -T | grep -E '^(kbdinteractive|authenticationmethods)'
```

### The thief tries again

```sh
# thief@thief-pc:~$
ssh ana@shop hostname
# ana@phone:~$
oathtool --totp -b "$(cat shop.key)"
# ana@laptop:~$
ssh shop hostname
# thief@thief-pc:~$
ssh ana@shop hostname
# ana@shop:~$
sudo journalctl -u ssh -o cat | grep -iE 'google|Accepted keyboard'
```

### Lost phones and limits

```sh
# ana@shop:~$
google-authenticator -t -d -f -r 3 -R 30 -w 3 -Q NONE
# ana@laptop:~$
ssh shop hostname
# ana@shop:~$
grep -c -E '^[0-9]{8}$' ~/.google_authenticator
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
