# SSH Keys vs Passwords: Which Is Safer for Security?

Video: https://youtu.be/1NcPZNT-1N8  
Written version: https://cloudexplainers.com/ssh-keys-vs-passwords-which-is-safer-for-security/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/common-logins.txt`](lab/common-logins.txt)
- [`lab/guess.sh`](lab/guess.sh)

## Commands, in the order the video runs them

### How SSH logs you in

```sh
# ana@laptop:~$
ssh shop
# ana@shop:~$
hostname
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

### Anyone can try a password

```sh
# thief@thief-pc:~$
cat common-logins.txt
guess shop common-logins.txt
# ana@shop:~$
sudo journalctl -u ssh -o cat | grep -E 'Failed|Accepted'
```

### How SSH keys work

```sh
# ana@laptop:~$
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
ssh-copy-id shop
# ana@shop:~$
cat ~/.ssh/authorized_keys
# ana@laptop:~$
ssh shop
eval "$(ssh-agent)"
ssh-add
ssh -v shop true 2>&1 | grep -E 'can continue|accepts key|Authenticated to'
```

### Why keys are safer

```sh
# ana@laptop:~$
python3 -c 'print(2**256)'
```

### Turn password login off

```sh
# ana@shop:~$
sudo sshd -T | grep passwordauthentication
sudo sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
grep -n '^PasswordAuthentication' /etc/ssh/sshd_config
sudo systemctl reload ssh
sudo sshd -T | grep passwordauthentication
# thief@thief-pc:~$
guess shop common-logins.txt
# ana@shop:~$
grep -n Include /etc/ssh/sshd_config
sudo grep -rn PasswordAuthentication /etc/ssh/sshd_config.d/
echo 'PasswordAuthentication no' | sudo tee /etc/ssh/sshd_config.d/00-keys-only.conf
sudo sshd -t && echo config OK
sudo systemctl reload ssh
sudo sshd -T | grep passwordauthentication
# thief@thief-pc:~$
guess shop common-logins.txt
# ana@laptop:~$
ssh shop hostname
```

### Keep your key safe

```sh
# ana@laptop:~$
ssh-keygen -y -f ~/.ssh/id_ed25519
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
