# The 7 Levels of Git

Video: https://youtu.be/5RvjReflx6w  
Written version: https://cloudexplainers.com/the-7-levels-of-git/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### The 7 levels of Git

```sh
# ana@ana-laptop:~/shop$
git diff
git restore index.html
```

### Level 1: Commits

```sh
# ana@ana-laptop:~/shop$
cat index.html
git init
ls -a
git status
git add index.html
git status
git commit -m "Create the shop homepage"
git log
```

### Level 2: Undo

```sh
# ana@ana-laptop:~/shop$
git status --short
cat index.html
git commit -am "Add a sale banner"
git revert HEAD --no-edit
git log --oneline
cat index.html
```

### Level 3: Branches

```sh
# ana@ana-laptop:~/shop$
git switch -c login-page
git add login.html
git commit -m "Add a login page"
git branch
git switch main
ls
git switch login-page
ls
```

### Level 4: Merging

```sh
# ana@ana-laptop:~/shop$
git switch main
git merge login-page
git switch -c summer-sale
git commit -am "Summer sale price for the blue kettle"
git switch main
git commit -am "Show that the blue kettle is in stock"
git merge summer-sale
cat index.html
cat index.html
git add index.html
git commit -m "Merge the summer sale"
git log --oneline --graph
```

### Level 5: Remotes

```sh
# ana@ana-laptop:~/shop$
git remote add origin git@git-server:shop.git
git push -u origin main
# ben@ben-laptop:~$
git clone git@git-server:shop.git
cd shop
# ben@ben-laptop:~/shop$
git log --oneline
git commit -am "Add a contact email"
git push
# ana@ana-laptop:~/shop$
git pull
tail -n 1 index.html
```

### Level 6: Teamwork

```sh
# ben@ben-laptop:~/shop$
git add faq.html
git commit -m "Add an FAQ page"
git push
# ana@ana-laptop:~/shop$
git commit -am "Add a log-in button"
git push
git pull
git pull --rebase
git push
git log --oneline -4
```

### Level 7: Rescue

```sh
# ana@ana-laptop:~/shop$
git reset --hard HEAD~3
git log --oneline -4
git reflog -5
git reset --hard HEAD@{1}
git log --oneline -4
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
