# Python Automation: Full Tutorial for Beginners

Video: https://youtu.be/Oq0RlbCNMqA  
Written version: https://cloudexplainers.com/python-automation-full-tutorial-for-beginners/

Everything below ran for real in the video. Run it in a throwaway machine or container, never on a computer you care about.

## Lab files

The machine the video used, as files you can build it from:

- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/make_files.py`](lab/make_files.py)
- [`lab/shop-bot/excel.py`](lab/shop-bot/excel.py)
- [`lab/shop-bot/invoices.py`](lab/shop-bot/invoices.py)
- [`lab/shop-bot/main.py`](lab/shop-bot/main.py)
- [`lab/shop-bot/portal.py`](lab/shop-bot/portal.py)
- [`lab/shop-bot/read_pdf.py`](lab/shop-bot/read_pdf.py)
- [`lab/shop-bot/report.py`](lab/shop-bot/report.py)
- [`lab/shop-bot/send.py`](lab/shop-bot/send.py)
- [`lab/shop-bot/stock.py`](lab/shop-bot/stock.py)
- [`lab/shop-bot/tidy.py`](lab/shop-bot/tidy.py)
- [`lab/supplier.py`](lab/supplier.py)

Build and open it (Docker):

```sh
docker build -t lab lab
docker run -it --rm lab bash
```

## Commands, in the order the video runs them

### Your weekly chores

```sh
# ana@laptop:~/shop-bot$
uv run main.py
```

### Set up with uv

```sh
# ana@laptop:~$
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv --version
uv init --no-package shop-bot
cd shop-bot
# ana@laptop:~/shop-bot$
ls -A
uv run main.py
uv add pandas openpyxl pypdf httpx playwright
cat pyproject.toml
ls -A
```

### Files with pathlib

```sh
# ana@laptop:~/shop-bot$
ls ~/Downloads | wc -l
ls ~/Downloads | head -4
ls ~/Downloads | tail -4
cat tidy.py
uv run tidy.py
ls ~/Downloads
ls ~/shop ~/shop/orders
```

### CSV and Excel

```sh
# ana@laptop:~/shop-bot$
head -4 ~/shop/orders/2026-10/orders-2026-10-01.csv
cat report.py
uv run report.py
cat excel.py
uv run excel.py
```

### Reading PDFs

```sh
# ana@laptop:~/shop-bot$
cat read_pdf.py
uv run read_pdf.py ~/shop/invoices/invoice-HL-1042.pdf
cat invoices.py
uv run invoices.py
```

### An API with httpx

```sh
# ana@laptop:~/shop-bot$
cat stock.py
uv run stock.py
export SUPPLIER_KEY=demo-key-123
uv run stock.py
```

### A website with Playwright

```sh
# ana@laptop:~/shop-bot$
uv run playwright install --with-deps chromium
head -n 17 portal.py
tail -n +18 portal.py
export PORTAL_PASSWORD=leaf-and-kettle
uv run portal.py
head -3 ~/shop/prices.csv
```

### Sending email

```sh
# ana@laptop:~/shop-bot$
head -n 20 send.py
tail -n +21 send.py
uv run send.py
grep -E '^(From|To|Subject|Content-Disposition):' /srv/mail/inbox.log
```

### On a schedule

```sh
# ana@laptop:~/shop-bot$
cat main.py
which uv
cat cron.txt
crontab cron.txt
date
cat bot.log
cat .env
cat cron.txt
crontab cron.txt
cat bot.log
grep -c '^Subject:' /srv/mail/inbox.log
crontab -l
```

---
From [Cloud Explainers](https://www.youtube.com/@cloudexplainers). Lab files are MIT licensed (see the repository's LICENSE).
