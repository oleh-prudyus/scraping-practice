from playwright.sync_api import sync_playwright

URL = "http://quotes.toscrape.com"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        quotes = page.locator(".quote").all()
        
        for quote in quotes:
            text = quote.locator(".text").text_content()
            author = quote.locator(".author").text_content()
            print(f"{text} - {author}")
            
        print(f"Count of quotes:{len(quotes)}")
        
        browser.close()


if __name__ == "__main__":
    main()
