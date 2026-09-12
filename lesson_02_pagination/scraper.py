from playwright.sync_api import sync_playwright
import csv

from typing_extensions import Writer

URL = "http://quotes.toscrape.com"


def main():
    collected = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        # TODO: в циклі - зібрати цитати з поточної сторінки,
        # перевірити чи є кнопка "Next", перейти далі або зупинитись
        
        exist = True
        
        while exist:
            quotes = page.locator(".quote").all()
            for quote in quotes:
                text = quote.locator(".text").text_content()
                author = quote.locator(".author").text_content()
                collected.append((text,author))
            
            next_button = page.locator(".next a")
            if next_button.count() > 0:
                next_button.click()
            else:
                exist = False
        
        browser.close()

    # TODO: записати collected у output/quotes.csv
        with open("output/quotes.csv","w",newline="",encoding="utf_8") as f:
            writer = csv.writer(f)
            writer.writerow(["text","author"])
            for text, author in collected:
                writer.writerow([text,author])

if __name__ == "__main__":
    main()
