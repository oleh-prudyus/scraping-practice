import os
import time

import requests

from bs4 import BeautifulSoup
import pandas as pd

URL = "http://quotes.toscrape.com"
SOURCE_CSV = "output/quotes_retry.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_with_retry(url, max_attempts=3):
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
       
        
    df = pd.DataFrame(collected, columns=["text","author"])
    df = df.drop_duplicates()   
    print(f"Shape: {df.shape}")
    print(f"Top authors: {df["author"].value_counts()}")
    print(f"Quotes of Albert Einstein:{df[df["author"]=="Albert Einstein"]}")
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/quotes_pandas.csv",index=False)


if __name__ == "__main__":
    main()
