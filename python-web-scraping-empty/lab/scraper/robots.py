from urllib.robotparser import RobotFileParser

bot = "tea-price-bot"
rules = RobotFileParser("http://shop.test/robots.txt")
rules.read()
for path in ["/api/teas", "/account/orders"]:
    print(path, "allowed:", rules.can_fetch(bot, "http://shop.test" + path))
print("Crawl delay:", rules.crawl_delay(bot), "second")
