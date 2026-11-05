# How Git Works

Video: https://youtu.be/qmv45R44jhc  
Written version: https://cloudexplainers.com/how-git-works/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Commands, in the order the video runs them

### Opening

```sh
# ana@ana-laptop:~/shop$
ls -a
git init
ls .git
```

### Blobs: content gets a name

```sh
# ana@ana-laptop:~/shop$
find .git/objects -type f | wc -l
git add menu.html about.html
find .git/objects -type f
git hash-object menu.html
git cat-file -t 20d4a29beb97cea29da9fc26087f865061fe21fc
git cat-file -p 20d4a29beb97cea29da9fc26087f865061fe21fc
wc -c menu.html
(printf 'blob %d\0' $(wc -c < menu.html); cat menu.html) | sha1sum
git ls-files --stage
```

### Trees and commits

```sh
# ana@ana-laptop:~/shop$
git commit -m 'Add the menu and about pages'
find .git/objects -type f
git cat-file -p HEAD
git cat-file -p HEAD^{tree}
git commit -am 'Raise matcha to $6'
git cat-file -p HEAD
git cat-file -p HEAD^{tree}
```

### Branches

```sh
# ana@ana-laptop:~/shop$
cat .git/HEAD
cat .git/refs/heads/main
git branch spring-menu
cat .git/refs/heads/spring-menu
wc -c .git/refs/heads/spring-menu
git switch spring-menu
cat .git/HEAD
git commit -am 'Add cherry blossom tea'
cat .git/refs/heads/main .git/refs/heads/spring-menu
git switch main
git merge spring-menu
cat .git/refs/heads/main
```

### Push

```sh
# ana@ana-laptop:~/shop$
git remote add origin git@git-server:shop.git
git push -u origin main
git commit -am 'Add oolong tea'
git push
# git@git-server:~/shop.git$
ls
cat refs/heads/main
git cat-file -t 0d4b325b80d6ce898e9f0331d3c10fe6462a72fd
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
