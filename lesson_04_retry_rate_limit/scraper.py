import csv
import os
import time

import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_with_retry(url, max_attempts=3):
    # TODO: спробувати requests.get(url, headers=HEADERS, timeout=10)
    # TODO: response.raise_for_status()
    # TODO: except requests.exceptions.RequestException -> retry з паузою, raise на останній спробі
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url,headers=HEADERS,timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Try: {attempt} invalid: {e}")
            if attempt == max_attempts:
                raise 
            time.sleep(2 ** attempt)
    


def main():
    collected = []
    page_num = 1

    while True:
        # TODO: print(f"Сторінка {page_num}...")
        # TODO: response = get_with_retry(f"{URL}/page/{page_num}/")
        # TODO: soup = BeautifulSoup(...)
        # TODO: quotes = soup.find_all(class_="quote")
        # TODO: if not quotes: break
        # TODO: зібрати text/author в collected
        # TODO: time.sleep(0.3) - пауза між сторінками
        # TODO: page_num += 1

        print(f"Сторінка {page_num}")
        response = get_with_retry(f"{URL}/page/{page_num}/")
        soup = BeautifulSoup(response.text,"html.parser")
        quotes = soup.find_all(class_="quote")
        
        if not quotes: break
        
        for quote in quotes:
            text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            collected.append((text, author))
            
        time.sleep(0.3)
        page_num += 1
        

    os.makedirs("output", exist_ok=True)
    with open("output/quotes_retry.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "author"])
        for text, author in collected:
            writer.writerow([text, author])


if __name__ == "__main__":
    main()
