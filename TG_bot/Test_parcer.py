from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://tracking.ozon.ru/?track=44612704-0204-1&local=zh-Hans&__rr=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)
    page.wait_for_timeout(10000)  # Ждём 10 секунд — пусть страница догрузится
    content = page.content()
    browser.close()

# Сохраняем страницу в файл, чтобы потом её открыть в браузере и проверить
with open("page.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Страница сохранена как page.html")
