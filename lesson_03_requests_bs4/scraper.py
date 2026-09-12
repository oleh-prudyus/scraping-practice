import csv
import os

import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com"


def main():
    collected = []
    
    page_num = 1
    while True:
        response = requests.get(f"{URL}/page/{page_num}/")
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        if not quotes:
            break

        for quote in quotes:
            text = quote.find("text").get_text()
            author = quote.find("author").get_text()
            collected.append((text, author))
            print(f"{text} -- {author}")
    page_num += 1


    os.makedirs("output", exist_ok=True)
    with open("output/quotes_bs4.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "author"])
        for text, author in collected:
            writer.writerow([text, author])
            

if __name__ == "__main__":
    main()
