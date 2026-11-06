from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://shop.test/")
    print("Teas found:", page.locator("li.tea").count())
    browser.close()
