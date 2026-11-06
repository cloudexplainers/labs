# Why Python Web Scraping Returns Nothing (and the Fix)

Video: https://youtu.be/k2QHyONLWzI  
Written version: https://cloudexplainers.com/why-python-web-scraping-returns-nothing-and-the-fix/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/scraper/api.py`](lab/scraper/api.py)
- [`lab/scraper/browser.py`](lab/scraper/browser.py)
- [`lab/scraper/fast.py`](lab/scraper/fast.py)
- [`lab/scraper/polite.py`](lab/scraper/polite.py)
- [`lab/scraper/robots.py`](lab/scraper/robots.py)
- [`lab/scraper/scrape.py`](lab/scraper/scrape.py)
- [`lab/scraper/too_soon.py`](lab/scraper/too_soon.py)
- [`lab/shop/server.py`](lab/shop/server.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Status 200, zero teas

```sh
# (.venv) ana@laptop:~/scraper$
cat scrape.py
python scrape.py
```

### What Python really downloads

```sh
# (.venv) ana@laptop:~/scraper$
curl -s http://shop.test/
curl -s http://shop.test/ | grep -c 'class="tea"'
# root@shop:/#
cat /var/log/shop.log
```

### Ask the API the page asks

```sh
# (.venv) ana@laptop:~/scraper$
curl -s http://shop.test/app.js | grep fetch
curl -s http://shop.test/api/teas | python -m json.tool | head -6
cat api.py
python api.py
```

### Let a real browser run it

```sh
# (.venv) ana@laptop:~/scraper$
cat browser.py
python browser.py
# root@shop:/#
cut -d' ' -f1-3 /var/log/shop.log
# (.venv) ana@laptop:~/scraper$
diff browser.py too_soon.py
python too_soon.py
time python api.py > /dev/null
time python browser.py > /dev/null
du -sh .venv/lib/python3.12/site-packages/httpx /ms-playwright/chromium_headless_shell-*
```

### Scrape like a good guest

```sh
# (.venv) ana@laptop:~/scraper$
curl -s http://shop.test/robots.txt
python robots.py
python fast.py
cat polite.py
python polite.py
# root@shop:/#
tail -n 2 /var/log/shop.log
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
