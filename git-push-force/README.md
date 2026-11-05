# Stop Using git push --force (Use This Instead)

Video: https://youtu.be/oXGJ-RGg5eA  
Written version: https://cloudexplainers.com/stop-using-git-push-force-use-this-instead/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### A lost commit

```sh
# ben@ben-laptop:~/shop$
git push
# ana@ana-laptop:~/shop$
git push --force
# ben@ben-laptop:~/shop$
git log --oneline origin/login-page
```

### Why Git refuses

```sh
# ana@ana-laptop:~/shop$
git log --oneline
git fetch
git rebase origin/main
git log --oneline
git push
```

### What --force does

```sh
# ben@ben-laptop:~/shop$
git commit -am "Add forgot-password link"
git fetch
git status
```

### Getting it back

```sh
# ben@ben-laptop:~/shop$
git rebase origin/login-page
git push
git log --oneline
```

### --force-with-lease

```sh
# ana@ana-laptop:~/shop$
git fetch
git rebase origin/main
# ben@ben-laptop:~/shop$
git commit -am "Show an error for a wrong password"
git push
# ana@ana-laptop:~/shop$
git push --force-with-lease
git rev-parse --short origin/login-page
```

### The background fetch

```sh
# ana@ana-laptop:~/shop$
git fetch
git push --force-with-lease --dry-run
```

### --force-if-includes

```sh
# ana@ana-laptop:~/shop$
git push --force-with-lease --force-if-includes
git pull --rebase
git rebase origin/main
git log --oneline
git push --force-with-lease --force-if-includes
# ben@ben-laptop:~/shop$
git log --oneline
```

### Make it the default

```sh
# ana@ana-laptop:~/shop$
git config --global alias.pushf "push --force-with-lease"
git config --global push.useForceIfIncludes true
git config --global --list | grep -i -e pushf -e useforce
git fetch
git pushf
```

### Protect main

```sh
# git@git-server:~/shop.git$
git config receive.denyNonFastForwards true
# ana@ana-laptop:~/shop$
git push --force
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
