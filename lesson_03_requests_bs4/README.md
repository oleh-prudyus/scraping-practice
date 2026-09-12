# Урок 3 — Requests & BeautifulSoup

Той самий сайт [quotes.toscrape.com](http://quotes.toscrape.com), але тепер без браузера — тільки HTTP-запит і парсинг HTML. Мета — відчути різницю в підході й API порівняно з Playwright.

## Завдання

1. Зробити GET-запит на `http://quotes.toscrape.com` через `requests`
2. Розпарсити відповідь через `BeautifulSoup`
3. Знайти всі цитати (`class="quote"`), вивести текст і автора кожної — як в уроці 1, але новим API
4. Зробити те саме з пагінацією — пройти всі сторінки (`/page/2/`, `/page/3/`, ...) і зібрати все в список
5. Зберегти результат у `output/quotes_bs4.csv` (як в уроці 2)

## Підказки

**Основні методи BeautifulSoup:**
```python
soup.find_all(class_="quote")      # всі елементи з класом .quote -> список
soup.find(class_="text")            # ПЕРШИЙ елемент з класом .text
element.get_text()                  # текст елемента (без HTML-тегів)
```
Зверни увагу: `class_` з підкресленням в кінці — бо `class` зарезервоване слово в Python (як і в C#), напряму використати не можна.

**Пагінація без кліків** — тут простіше, ніж з Playwright: просто підставляй номер сторінки в URL і роби новий запит:
```python
for page_num in range(1, 11):
    response = requests.get(f"http://quotes.toscrape.com/page/{page_num}/")
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all(class_="quote")
    if not quotes:
        break   # сторінки закінчились
    ...
```

**Встанови нові залежності** (додані в `requirements.txt`):
```bash
pip install -r requirements.txt
```

## Критерій виконання

```bash
python lesson_03_requests_bs4/scraper.py
```
Створює `output/quotes_bs4.csv` з тим самим набором цитат, що й у 2-му уроці (100 штук), але без запуску браузера — помітно швидше.
