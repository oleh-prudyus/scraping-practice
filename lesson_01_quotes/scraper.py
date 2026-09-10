from playwright.sync_api import sync_playwright

URL = "http://quotes.toscrape.com"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        # TODO: знайти всі елементи .quote
        # TODO: для кожного вивести текст (.text) і автора (.author)
        # TODO: порахувати і вивести загальну кількість

        browser.close()


if __name__ == "__main__":
    main()
