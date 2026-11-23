# How to Fix MySQL Database Error 1045: Access Denied for User

Video: https://youtu.be/NYvhaO5f3F8  
Written version: https://cloudexplainers.com/how-to-fix-mysql-database-error-1045-access-denied-for-user/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/board/Dockerfile`](lab/board/Dockerfile)
- [`lab/board/board/board.ini`](lab/board/board/board.ini)
- [`lab/board/board/board.py`](lab/board/board/board.py)
- [`lab/laptop/Dockerfile`](lab/laptop/Dockerfile)
- [`lab/laptop/testdb/compose.yaml`](lab/laptop/testdb/compose.yaml)
- [`lab/server/Dockerfile`](lab/server/Dockerfile)

## Commands, in the order the video runs them

### The password is right, still denied

```sh
# trish@board:~/board$
python3 board.py
cat board.ini
# trish@dispatch-db:~$
mysql -u dispatch -p -e 'SELECT CURRENT_USER()'
```

### Same user, another host

```sh
# trish@dispatch-db:~$
sudo mysql -e "SELECT user, host FROM mysql.user WHERE user = 'dispatch'"
sudo mysql
mysql> ALTER USER 'dispatch'@'%' IDENTIFIED BY 'Pipe$Wrench9';
mysql> exit
# trish@board:~/board$
python3 board.py
```

### using password: NO

```sh
# trish@board:~/board$
python3 board.py
grep -n password board.ini
```

### The shell changed the password

```sh
# trish@dispatch-db:~$
mysql -u dispatch -p"Pipe$Wrench9" -e 'SELECT CURRENT_USER()'
echo "Pipe$Wrench9"
mysql -u dispatch -p'Pipe$Wrench9' -e 'SELECT CURRENT_USER()'
```

### Typos, and root on Ubuntu

```sh
# trish@dispatch-db:~$
mysql -u dispach -p -e 'SELECT CURRENT_USER()'
mysql -u root -p
sudo mysql -e "SELECT user, host, plugin FROM mysql.user WHERE user = 'root'"
```

### Docker kept the old password

```sh
# mike@laptop:~/testdb$
grep ROOT compose.yaml
docker compose up -d
docker compose exec db mysql -uroot -pTap-Washer-12 -e 'SELECT 1'
docker compose exec db mysql -uroot -pfirst-test-pw -e 'SELECT CURRENT_USER()'
docker compose exec db mysql -uroot -pfirst-test-pw -e "ALTER USER 'root'@'%' IDENTIFIED BY 'Tap-Washer-12'; ALTER USER 'root'@'localhost' IDENTIFIED BY 'Tap-Washer-12'"
docker compose exec db mysql -uroot -pTap-Washer-12 -e 'SELECT CURRENT_USER()'
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
