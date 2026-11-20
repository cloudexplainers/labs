# Git and GitHub: Full Tutorial for Beginners

Video: https://youtu.be/cLcb6yuZW2Y  
Written version: https://cloudexplainers.com/git-and-github-full-tutorial-for-beginners/

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

### Three classes, gone

```sh
# ana@ana-laptop:~/pottery-site$
git diff
git restore index.html
git status
```

### What Git and GitHub are

```sh
# ana@ana-laptop:~$
git --version
```

### Your first repository

```sh
# ana@ana-laptop:~$
mkdir pottery-site && cd pottery-site
# ana@ana-laptop:~/pottery-site$
ls
git status
git init
git branch -m main
git config --global init.defaultBranch main
ls -a
git status
```

### Your first commit

```sh
# ana@ana-laptop:~/pottery-site$
git add index.html
git status
git add .
git commit -m 'First version of the class page'
git config --global user.name 'Ana'
git config --global user.email ana@example.com
git commit -m 'First version of the class page'
git log
git status
```

### Saving each change

```sh
# ana@ana-laptop:~/pottery-site$
git status
git diff
git add index.html
git diff
git diff --staged
git commit -m 'Add the Saturday famly class'
git commit --amend -m 'Add the Saturday family class'
git log --oneline
```

### Files Git should skip

```sh
# ana@ana-laptop:~/pottery-site$
git status
cat .gitignore
git status
git add .gitignore
git commit -m 'Keep drafts out of Git'
```

### Undoing a mistake

```sh
# ana@ana-laptop:~/pottery-site$
git add .
git status
git restore --staged test.html
git status
rm test.html
git commit -am 'Update hand building price'
git show --oneline HEAD
git revert --no-edit HEAD
git log --oneline
grep Thursday index.html
git show 367e254:index.html | grep '<li>'
```

### Branches

```sh
# ana@ana-laptop:~/pottery-site$
git branch
git switch -c glaze-workshop
git commit -am 'Add the Sunday glazing workshop'
git log --oneline --graph --all
git switch main
grep -c Sunday index.html
git merge glaze-workshop
grep -c Sunday index.html
git branch -d glaze-workshop
```

### When two changes collide

```sh
# ana@ana-laptop:~/pottery-site$
git switch -c spring-prices
git commit -am 'Spring price for the wheel class'
git switch main
git switch spring-prices
git stash
git switch spring-prices
grep Tuesday index.html
git switch main
git stash pop
git commit -am 'Move the wheel class to 7pm'
git merge spring-prices
git status
cat index.html
grep Tuesday index.html
git add index.html
git commit --no-edit
git log --oneline --graph -6
```

### Putting it on GitHub

```sh
# ana@ana-laptop:~/pottery-site$
gh repo create cloudexplainers/pottery-class-site --private
git remote add origin https://github.com/cloudexplainers/pottery-class-site.git
git remote -v
git push -u origin main
git status
# ben@ben-laptop:~$
git clone https://github.com/cloudexplainers/pottery-class-site.git
cd pottery-class-site
# ben@ben-laptop:~/pottery-class-site$
git config --global user.name 'Ben' && git config --global user.email ben@example.com
git log --oneline -3
```

### Working with someone else

```sh
# ben@ben-laptop:~/pottery-class-site$
git commit -am 'Add how to book'
git push
# ana@ana-laptop:~/pottery-site$
git pull
git commit -am 'Green heading'
# ben@ben-laptop:~/pottery-class-site$
git commit -am 'New phone number'
git push
# ana@ana-laptop:~/pottery-site$
git push
git pull
git config --global pull.rebase false
git pull
git push
```

### Pull requests

```sh
# ben@ben-laptop:~/pottery-class-site$
git pull
git switch -c friday-class
git commit -am 'Add the Friday date night class'
git push -u origin friday-class
gh pr create --title 'Add the Friday date night class' --body 'Ana: can you check the price?'
# ana@ana-laptop:~/pottery-site$
gh pr list
gh pr diff 1
gh pr comment 1 --body 'Looks good. Can we make it $65?'
# ben@ben-laptop:~/pottery-class-site$
git commit -am 'Date night: $65'
git push
# ana@ana-laptop:~/pottery-site$
gh pr diff 1
gh pr merge 1 --merge --delete-branch
git pull
git log --oneline --graph -6
```

### The everyday loop

```sh
# ana@ana-laptop:~/pottery-site$
git blame --date=short index.html
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
