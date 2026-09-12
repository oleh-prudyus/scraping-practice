import time

import requests
from bs4 import BeautifulSoup

from .config import SOURCE_URL, logger

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_with_retry(url, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"Спроба {attempt} для {url} невдала: {e}")
            if attempt == max_attempts:
                raise
            time.sleep(2 ** attempt)


def scrape_quotes():
    collected = []
    page_num = 1

    while True:
        response = get_with_retry(f"{SOURCE_URL}/page/{page_num}/")
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        if not quotes:
            break

        for quote in quotes:
            text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            collected.append((text, author))

        time.sleep(0.3)
        page_num += 1

    return collected
