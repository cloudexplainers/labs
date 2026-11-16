# How to Fix GitHub 'Permission Denied (publickey)' Errors

Video: https://youtu.be/yn27SiPDQvs  
Written version: https://cloudexplainers.com/how-to-fix-github-permission-denied-publickey-errors/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/gitserve`](lab/gitserve)
- [`lab/sshd_config`](lab/sshd_config)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Permission denied (publickey)

```sh
# ana@club-laptop:~$
git clone git@github.com:cloudexplainers/labs.git
git clone https://github.com/cloudexplainers/labs.git
```

### The fix: a key, and its public half on file

```sh
# ana@club-laptop:~$
git clone git@git-server:sailing-club/results.git
ssh-keygen -t ed25519 -C "ana@sailing-club"
git clone git@git-server:sailing-club/results.git
ssh -v -T git@git-server 2>&1 | grep -E 'Offering|Authentications that|denied'
cat ~/.ssh/id_ed25519.pub
ssh -T git@git-server
git clone git@git-server:sailing-club/results.git
# ana@club-laptop:~/results$
git push
```

### Test it without Git

```sh
# ana@club-laptop:~$
ssh -T git@github.com
ssh -v -T git@github.com 2>&1 | grep -E 'identity file|Authentications that|No more|denied'
```

### A key ssh ignores

```sh
# ana@club-laptop:~/results$
chmod 644 ~/.ssh/id_ed25519
git pull
ls -l ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519
git pull
```

### sudo and Git

```sh
# ana@club-laptop:~/results$
sudo git pull
sudo ls -a /root/.ssh
```

### A key under another name

```sh
# ben@club-laptop:~$
ssh-keygen -t ed25519 -C "ben@sailing-club"
git clone git@git-server:sailing-club/results.git
ssh -v -T git@git-server 2>&1 | grep -E 'identity file|denied'
ssh -T git@git-server
git clone git@git-server:sailing-club/results.git
```

### Always the git user

```sh
# ben@club-laptop:~$
ssh -T ben@git-server
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
