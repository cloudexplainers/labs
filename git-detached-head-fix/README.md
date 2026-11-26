# How to Fix Git 'Detached HEAD' State

Video: https://youtu.be/C9BcYYMhTOo  
Written version: https://cloudexplainers.com/how-to-fix-git-detached-head-state/

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

### Where did the commit go?

```sh
# jess@laptop:~/timetable$
git switch main
git log --oneline --graph --all
```

### What HEAD points to

```sh
# jess@laptop:~/timetable$
git log --oneline --decorate
cat .git/HEAD
cat .git/refs/heads/main
git checkout v1.2
git status
git branch
cat timetable.html
git commit -am 'Fix the Sunday departure time'
git log --oneline --decorate -3
```

### Getting the commit back

```sh
# jess@laptop:~/timetable$
git reflog -3
git show --stat --oneline ea050c9
git branch sunday-fix ea050c9
git log --oneline --graph --all
git merge sunday-fix
grep Sunday timetable.html
```

### Other ways in

```sh
# jess@laptop:~/timetable$
git checkout 2289b49
git switch -
git checkout origin/main
git status
```

### Never lose one again

```sh
# jess@laptop:~/timetable$
git switch v1.2
git switch -c poster-fix v1.2
cat .git/HEAD
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
