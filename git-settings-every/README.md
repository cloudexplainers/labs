# Every Git Setting to Change on Day One

Video: https://youtu.be/6X7UmIE5aew  
Written version: https://cloudexplainers.com/every-git-setting-to-change-on-day-one/

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

### Zero settings

```sh
git commit -am 'Swap dishes and laundry'
# linda@laptop:~$
git config --global --list
```

### user.name and user.email

```sh
# linda@laptop:~/chores$
git log -1 --format='%h %an <%ae>'
git config --global user.name "Linda"
git config --global user.email linda@example.com
git commit --amend --reset-author --no-edit
git log -1 --format='%h %an <%ae>'
git config --show-origin user.email
```

### init.defaultBranch

```sh
git init recipes
# linda@laptop:~$
git config --global init.defaultBranch main
git init meal-plan
git -C meal-plan branch --show-current
```

### pull.rebase

```sh
# linda@laptop:~/chores$
git commit -am 'Add Sunday chores'
git pull
# linda@laptop:~/chores$
git config --global pull.rebase true
git pull
git log --oneline --graph -4
```

### rebase.autoStash

```sh
# linda@laptop:~/chores$
git status --short
git pull
git config --global rebase.autoStash true
git pull
# linda@laptop:~/chores$
git status --short
git commit -am 'Towels on Sunday too'
git push
```

### push.autoSetupRemote

```sh
# linda@laptop:~/chores$
git switch -c holiday-rota
git add holiday.md
git commit -m 'Add the holiday rota'
git push
# linda@laptop:~/chores$
git config --global push.autoSetupRemote true
git push
```

### fetch.prune

```sh
# linda@laptop:~/chores$
git fetch
git branch -r
git config --global fetch.prune true
git fetch
git branch -r
```

### merge.conflictStyle

```sh
# linda@laptop:~/chores$
git commit -am 'Take turns with the bins'
git fetch
git merge origin/main
cat chores.md
# linda@laptop:~/chores$
git merge --abort
git config --global merge.conflictStyle zdiff3
git merge origin/main
cat chores.md
# linda@laptop:~/chores$
git add chores.md
git commit --no-edit
```

### help.autocorrect

```sh
# linda@laptop:~/chores$
git stauts
git config --global help.autocorrect prompt
git stauts
```

### Sunday night

```sh
git pull
# rob@laptop:~/chores$
git log --format='%h %an <%ae>' -6
```

### Recap

```sh
# linda@laptop:~/chores$
cat ~/.gitconfig
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
