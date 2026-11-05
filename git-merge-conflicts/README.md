# How to Fix Git Merge Conflicts

Video: https://youtu.be/D2oPNUr5CbA  
Written version: https://cloudexplainers.com/how-to-fix-git-merge-conflicts/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### A pull that stopped

```sh
# ana@ana-laptop:~/shop$
git pull
cat menu.html
```

### Read the conflict

```sh
# ana@ana-laptop:~/shop$
git status
git diff --check
```

### Not ready? Back out

```sh
# ana@ana-laptop:~/shop$
git merge --abort
git status
cat menu.html
```

### Fix the file

```sh
# ana@ana-laptop:~/shop$
git config --global merge.conflictStyle zdiff3
git config --global rerere.enabled true
git pull
git diff --check
git add menu.html
git status
git commit --no-edit
```

### Conflicts in a rebase

```sh
# ana@ana-laptop:~/shop$
git fetch
git rebase origin/main
cat menu.html
git add menu.html
git rebase --continue
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
