# How to Fix Git 'Updates Were Rejected' When You Push

Video: https://youtu.be/jIFuF2S49zU  
Written version: https://cloudexplainers.com/how-to-fix-git-updates-were-rejected-when-you-push/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Updates were rejected

```sh
# ana@ana-laptop:~/station$
git push
git push
cat schedule.html about.html
```

### The quick fix: pull with rebase, then push

```sh
# ana@ana-laptop:~/station$
git pull --rebase
git log --oneline --graph
```

### What your laptop didn't know

```sh
# ana@ana-laptop:~/station$
git status
git fetch
git status
git log --oneline --graph --all
```

### After you rewrote a pushed commit

```sh
# ana@ana-laptop:~/station$
git commit -a --amend --no-edit
git status
git push
git push --force-with-lease
```

### Why plain git pull refused

```sh
# ana@ana-laptop:~/station$
git pull
```

### A new repository with a README

```sh
# ana@ana-laptop:~/playlist$
git push -u origin main
git pull --no-rebase origin main
git pull origin main
ls
git push -u origin main
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
