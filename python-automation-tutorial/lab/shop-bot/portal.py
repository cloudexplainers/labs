import os
from pathlib import Path

from playwright.sync_api import sync_playwright

shop = Path.home() / "shop"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()  # headless: no window
        page = browser.new_page()
        page.goto("http://localhost:8000/portal")
        page.get_by_label("Username").fill("ana")
        page.get_by_label("Password").fill(os.environ["PORTAL_PASSWORD"])
        page.get_by_role("button", name="Sign in").click()

        page.wait_for_url("**/deliveries")
        for row in page.locator("table tr").all()[1:]:
            print("Delivery:", row.inner_text().replace("\t", " | "))
        with page.expect_download() as download:
            page.get_by_text("Download price list").click()
        download.value.save_as(shop / "prices.csv")
        page.screenshot(path=shop / "portal.png")
        browser.close()
    print("Saved prices.csv and portal.png")


if __name__ == "__main__":
    run()
