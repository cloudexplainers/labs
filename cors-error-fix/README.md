# How to Fix API CORS Errors: No 'Access-Control-Allow-Origin'

Video: https://youtu.be/Y5AJnHVZY6E  
Written version: https://cloudexplainers.com/how-to-fix-api-cors-errors-no-access-control-allow-origin/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/api/surf-api.service`](lab/api/surf-api.service)
- [`lab/api/surf_api.py`](lab/api/surf_api.py)
- [`lab/nginx/log.conf`](lab/nginx/log.conf)
- [`lab/nginx/step1.conf`](lab/nginx/step1.conf)
- [`lab/nginx/step2.conf`](lab/nginx/step2.conf)
- [`lab/nginx/step3.conf`](lab/nginx/step3.conf)
- [`lab/nginx/step4.conf`](lab/nginx/step4.conf)
- [`lab/nginx/surfschool.conf`](lab/nginx/surfschool.conf)
- [`lab/site/app.js`](lab/site/app.js)
- [`lab/site/index.html`](lab/site/index.html)
- [`lab/site/style.css`](lab/site/style.css)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Data in curl, blocked in the browser

```sh
# ana@surfschool:~$
curl -s http://api.surf.test/lessons
sudo tail -n 2 /var/log/nginx/api.log
```

### The quick fix: one header

```sh
# ana@surfschool:~$
curl -sI -H "Origin: http://www.surf.test" http://api.surf.test/lessons
grep -n add_header /etc/nginx/sites-available/surfschool.conf
sudo nginx -t && sudo systemctl reload nginx
```

### The request before the request

```sh
# ana@surfschool:~$
sudo tail -n 3 /var/log/nginx/api.log
grep -n add_header /etc/nginx/sites-available/surfschool.conf
sudo tail -n 2 /var/log/nginx/api.log
```

### The same error, from a full lesson

```sh
# ana@surfschool:~$
sudo tail -n 2 /var/log/nginx/api.log
curl -si -X POST -H "Origin: http://www.surf.test" -b session=maya-7f3a -H 'Content-Type: application/json' -d '{"lesson": 1}' http://api.surf.test/bookings
```

### Check it from a terminal

```sh
# ana@surfschool:~$
curl -si -X OPTIONS -H "Origin: http://www.surf.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: content-type" http://api.surf.test/bookings
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
